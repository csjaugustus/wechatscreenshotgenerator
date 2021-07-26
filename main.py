from imageProcessing import Screenshot
import re
import os
from tkinter import *
from PIL import Image, ImageTk
from datetime import datetime

def getTimestamp():
	now = datetime.now()
	dt_string = now.strftime("%Y%d%m%H%M")
	return dt_string

def updatePreview():
	currentCanvas = canvas.get()
	imagePreview = currentCanvas.resize((round(w/3), round(h/3)))
	imagePreview = ImageTk.PhotoImage(imagePreview)
	imagePreviewWidget.configure(image=imagePreview)
	imagePreviewWidget.image = imagePreview
	imagePreviewWidget.grid(row=1, column=0)

def popupMessage(title, message, windowToClose=None):
	popupWindow = Toplevel()
	popupWindow.title(title)
	if not windowToClose:
		close = popupWindow.destroy
	elif windowToClose == 'all':
		close = popupWindow.quit
	else:
		def close():
			popupWindow.destroy()
			windowToClose.destroy()
	msg = Label(popupWindow, text=message, padx=10, pady=10)
	ok = Button(popupWindow, text="Ok", padx=10,
				pady=10, command=close)
	msg.pack()
	ok.pack()
	

def addEntry():
	def confirm():
		if cbVar.get():
			timeRegex = re.compile('^\\d{2}:\\d{2}$')
			text = e2.get("1.0", END)
			errors = []
			if not text:
				errors.append("Please enter some text.")
			elif not timeRegex.findall(text):
				errors.append("Please enter a valid time in such format xx:xx.")
			if errors:
				popupMessage("Error", "\n".join(e for e in errors))
				return

			canvas.addTimeMarker(text)
			addWindow.destroy()

		else:
			side = var.get()
			text = e2.get("1.0", END)
			avyName = e1.get()

			#check for errors
			errors = []
			if side not in ("left", "right"):
				errors.append("Please select left or right.")
			if not avyName:
				errors.append("Please select an avatar.")
			if not text:
				errors.append("Please enter some text.")
			if errors:
				popupMessage("Error", "\n".join(e for e in errors))
				return

			canvas.add(avyName, text, side)
			addWindow.destroy()

		lb.insert(END, text)
		clearButton.config(state=NORMAL)
		deleteButton.config(state=NORMAL)
		saveButton.config(state=NORMAL)
		saveIndividualButton.config(state=NORMAL)

		updatePreview()

	def selectAvatar(x):
		e1.config(state=NORMAL)
		e1.delete(0, END)
		e1.insert(0, x)
		e1.config(state=DISABLED)

	if not os.listdir("files\\avatars"):
		popupMessage("Error", "No avatar image found. Please add at least one avatar image in files\\avatars.")
		return

	addWindow = Toplevel()
	addWindow.title("Add Entry")
	r, c = 0, 0

	avyButtons = []
	for avyName in os.listdir("files\\avatars"):
		avyImage = Image.open(f"files\\avatars\\{avyName}")
		avyImage = avyImage.resize((50,50))
		avyImage = ImageTk.PhotoImage(avyImage)
		b = Button(addWindow, image=avyImage, command=lambda x=avyName:selectAvatar(x))
		b.image = avyImage
		avyButtons.append(b)
		b.grid(row=r, column=c)
		c += 1
		if c == 4:
			c = 0
			r += 1

	l1 = Label(addWindow, text="Avatar Selected:", padx=10)
	e1 = Entry(addWindow, width=30)
	l1.grid(row=0, column=4)
	e1.grid(row=0, column=5, columnspan=2)
	e1.config(state=DISABLED)

	l2 = Label(addWindow, text="Text:", padx=10)
	e2 = Text(addWindow, height=10, width=30)
	l2.grid(row=1, column=4)
	e2.grid(row=1, column=5,columnspan=2)

	l3 = Label(addWindow, text="Side:", padx=10)
	var = StringVar()
	var.set(' ')
	r1 = Radiobutton(addWindow, text="Left", variable=var, value="left")
	r2 = Radiobutton(addWindow, text="Right", variable=var, value="right")
	l3.grid(row=2,column=4)
	r1.grid(row=2, column=5)
	r2.grid(row=2, column=6)

	def changeStates(event):
		if r1['state'] == NORMAL:
			r1.config(state=DISABLED)
			r2.config(state=DISABLED)
			e1.delete(0, END)
			for b in avyButtons:
				b.config(state=DISABLED)
		else:
			r1.config(state=NORMAL)
			r2.config(state=NORMAL)
			for b in avyButtons:
				b.config(state=NORMAL)

	cbVar = IntVar()
	cb = Checkbutton(addWindow, text="Add as Time Marker", variable=cbVar, padx=10)
	cb.grid(row=3, column=4, columnspan=3)
	cb.bind('<Button-1>', changeStates)

	confirmButton = Button(addWindow, text="Confirm", command=confirm, padx=10, pady=10)
	confirmButton.grid(row=4, column=4, columnspan=3)
	r1.select()


def deleteEntry():
	selectedIndex = lb.curselection()
	if not selectedIndex:
		popupMessage("Nothing selected",
					 "Please select an entry to delete.")
	else:
		selectedIndex = selectedIndex[0]
		canvas.delete(selectedIndex)
		lb.delete(selectedIndex)

		if not lb.get(0):
			if not canvas.title:
				clearButton.config(state=DISABLED)
				deleteButton.config(state=DISABLED)
				saveButton.config(state=DISABLED)
				saveIndividualButton.config(state=DISABLED)

		updatePreview()

def saveScreenshot():
	d = f"output\\SS-{getTimestamp()}.png"
	currentCanvas = canvas.get()
	currentCanvas.save(d)
	popupMessage("Successful", f"Saved under {d}.")
	

def setTitle():
	title = titleEntry.get()
	canvas.setTitle(title)
	updatePreview()

	if title:
		clearButton.config(state=NORMAL)
	else:
		if not lb.get(0):
			clearButton.config(state=DISABLED)
			deleteButton.config(state=DISABLED)
			saveButton.config(state=DISABLED)
			saveIndividualButton.config(state=DISABLED)			

def saveIndividual():
	selectedIndex = lb.curselection()
	if not selectedIndex:
		popupMessage("Nothing selected", "Please select an entry to save.")
	else:
		selectedIndex = selectedIndex[0]
		if canvas.mode == "light":
			toSave = canvas.entries[selectedIndex]
		elif canvas.mode == "dark":
			toSave = canvas.entriesDark[selectedIndex]
		d = f"output\\B{selectedIndex}-{getTimestamp()}.png"
		toSave.save(d)
		popupMessage("Successful", f"Saved under {d}.")

def openDir():
	os.startfile(os.getcwd())

def clear():
	def clearScreen():
		confirmation.destroy()
		canvas.entries.clear()
		canvas.entriesDark.clear()
		lb.delete(0,'end')
		canvas.setTitle("")
		canvas.update()
		updatePreview()

	confirmation = Toplevel()
	confirmation.title("Confirmation")
	l = Label(confirmation, text="Are you sure you want to clear the screenshot?\nAll unsaved bubbles will be erased.")
	b1 = Button(confirmation, text="Yes", command=clearScreen, padx=10)
	b2 = Button(confirmation, text="No", command=confirmation.destroy, padx=10)
	l.grid(row=0,column=0,columnspan=3)
	b1.grid(row=1,column=0)
	b2.grid(row=1,column=2)

	clearButton.config(state=DISABLED)
	deleteButton.config(state=DISABLED)
	saveButton.config(state=DISABLED)
	saveIndividualButton.config(state=DISABLED)

def changeMode(event):
	if canvas.mode == "light":
		canvas.mode = "dark"
	else:
		canvas.mode = "light"
	canvas.setMode()
	canvas.update(changeMode=True)
	updatePreview()

width = 864
maxChatHeight = 1684

if "output" not in os.listdir():
	os.mkdir("output")

root = Tk()
root.title("WeChat Screenshot Generator")
icon = Image.open("files\\wechat-logo.png")
icon = ImageTk.PhotoImage(icon)
root.iconphoto(True, icon)

canvas = Screenshot('light')
currentCanvas = canvas.get()
w, h = currentCanvas.size
imagePreview = currentCanvas.resize((round(w/3), round(h/3)))
imagePreview = ImageTk.PhotoImage(imagePreview)
imagePreviewWidget = Label(root, image=imagePreview, borderwidth=2, relief="sunken")
folderIcon = Image.open("files\\foldericon.png")
folderIcon = folderIcon.resize((25,25))
folderIcon = ImageTk.PhotoImage(folderIcon)

saveButton = Button(root, text="Save Screenshot", padx=10, pady=10, command=saveScreenshot)
setTitleLabel = Label(root, text="Chat Title:", padx=10, pady=10)
setTitleButton = Button(root, text="Set", padx=10, command=setTitle)
titleEntry = Entry(root, width=20)
lb = Listbox(root, height=35, width=50)
addButton = Button(root, text="Add", padx=10, pady=10, command=addEntry)
deleteButton = Button(root, text="Delete", padx=10, pady=10, command=deleteEntry)
saveIndividualButton = Button(root, text="Save Selected Bubble", padx=10, pady=10, command=saveIndividual)
openDirectoryButton = Button(root, image=folderIcon, command=openDir)
openDirectoryButton.image = folderIcon
clearButton = Button(root, text="Clear", padx=10, pady=10, command=clear)
mode = IntVar()
darkMode = Checkbutton(root, text="Dark Mode", padx=10, variable=mode)
darkMode.bind('<Button-1>', changeMode)

clearButton.config(state=DISABLED)
deleteButton.config(state=DISABLED)
saveButton.config(state=DISABLED)
saveIndividualButton.config(state=DISABLED)

imagePreviewWidget.grid(row=1, column=0, columnspan=2)
darkMode.grid(row=0,column=0, columnspan=2)
setTitleLabel.grid(row=0, column=2)
titleEntry.grid(row=0,column=3)
setTitleButton.grid(row=0, column=4)
lb.grid(row=1,column=2, columnspan=4)
saveButton.grid(row=2,column=1)
addButton.grid(row=2, column=2)
deleteButton.grid(row=2,column=3)
saveIndividualButton.grid(row=2,column=4,columnspan=2)
openDirectoryButton.grid(row=0,column=5)
clearButton.grid(row=2,column=0)


root.mainloop()