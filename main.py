from imageProcessing import createBubble, loadAvatar, get_concat_v, drawTitle
import os
from tkinter import *
from PIL import Image, ImageTk
from datetime import datetime

def getTimestamp():
	now = datetime.now()
	dt_string = now.strftime("%Y%d%m%H%M")
	return dt_string

def updatePreview():
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
		side = var.get()
		text = e2.get("1.0", END)
		avyName = e1.get()

		#check for errors
		errors = []
		if side not in ("left", "right"):
			errors.append("Please select left or right.")
		if not avyName:
			errors.append("Please select an avatar.")
		if errors:
			popupMessage("Error", "\n".join(e for e in errors))
			return

		avatar = loadAvatar(f"files\\avatars\\{avyName}")
		bubble = createBubble(avatar, text, side)
		addWindow.destroy()
		entries.append(bubble)

		#update current canvas
		img = entries[0]
		if len(entries) > 1:
			for i in range(1, len(entries)):
				img = get_concat_v(img, entries[i])
		if img.size[1] > maxChatHeight:
			img = img.crop((0, img.size[1]-maxChatHeight, width, img.size[1]))
		currentCanvas.paste(img, (0,113))

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

	for avyName in os.listdir("files\\avatars"):
		avyImage = Image.open(f"files\\avatars\\{avyName}")
		avyImage = avyImage.resize((50,50))
		avyImage = ImageTk.PhotoImage(avyImage)
		b = Button(addWindow, image=avyImage, command=lambda x=avyName:selectAvatar(x))
		b.image = avyImage
		b.grid(row=r, column=c)
		c += 1
		if c == 4:
			c = 0
			r += 1

	l1 = Label(addWindow, text="Avatar Selected:", padx=10)
	e1 = Entry(addWindow, width=30)
	l1.grid(row=0, column=4)
	e1.grid(row=0, column=5)
	e1.config(state=DISABLED)

	l2 = Label(addWindow, text="Text:", padx=10)
	e2 = Text(addWindow, height=10, width=30)
	l2.grid(row=1, column=4)
	e2.grid(row=1, column=5)

	var = StringVar()
	var.set(' ')
	r1 = Radiobutton(addWindow, text="Left", variable=var, value="left")
	r2 = Radiobutton(addWindow, text="Right", variable=var, value="right")
	r1.grid(row=2, column=4)
	r2.grid(row=2, column=5)

	confirmButton = Button(addWindow, text="Confirm", command=confirm, padx=10, pady=10)
	confirmButton.grid(row=3, column=4, columnspan=2)


def deleteEntry():
	selectedIndex = lb.curselection()
	if not selectedIndex:
		popupMessage("Nothing selected",
					 "Please select an entry to delete.")
	else:
		selectedIndex = selectedIndex[0]
		del entries[selectedIndex]
		lb.delete(selectedIndex)

		if not lb.get(0):
			clearButton.config(state=DISABLED)
			deleteButton.config(state=DISABLED)
			saveButton.config(state=DISABLED)
			saveIndividualButton.config(state=DISABLED)

		#update current canvas
		blank = Image.new('RGB', (width,maxChatHeight), color=(237,237,237))
		currentCanvas.paste(blank, (0,113))

		if entries:
			img = entries[0]
			if len(entries) > 1:
				for i in range(1, len(entries)):
					img = get_concat_v(img, entries[i])
			if img.size[1] <= maxChatHeight:
				currentCanvas.paste(img,(0,113))

		updatePreview()

def saveScreenshot():
	d = f"output\\SS-{getTimestamp()}.png"
	currentCanvas.save(d)
	popupMessage("Successful", f"Saved under {d}.")
	

def setTitle(currentCanvas):
	title = titleEntry.get()
	currentCanvas = drawTitle(currentCanvas, title)
	updatePreview()

def saveIndividual():
	selectedIndex = lb.curselection()
	if not selectedIndex:
		popupMessage("Nothing selected", "Please select an entry to save.")
	else:
		selectedIndex = selectedIndex[0]
		toSave = entries[selectedIndex]
		d = f"output\\B{selectedIndex}-{getTimestamp()}.png"
		toSave.save(d)
		popupMessage("Successful", f"Saved under {d}.")

def openDir():
	os.startfile(os.getcwd())

def clear():
	def clearScreen():
		confirmation.destroy()
		entries.clear()
		lb.delete(0,'end')
		blank = Image.new('RGB', (width,maxChatHeight), color=(237,237,237))
		currentCanvas.paste(blank, (0,113))
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

width = 864
maxChatHeight = 1684
entries = []

if "output" not in os.listdir():
	os.mkdir(output)

root = Tk()
root.title("WeChat Screenshot Generator")
icon = Image.open("files\\wechat-logo.png")
icon = ImageTk.PhotoImage(icon)
root.iconphoto(True, icon)

currentCanvas = Image.open("files\\blankScreenshot.png")
w, h = currentCanvas.size
imagePreview = currentCanvas.resize((round(w/3), round(h/3)))
imagePreview = ImageTk.PhotoImage(imagePreview)
imagePreviewWidget = Label(root, image=imagePreview)
folderIcon = Image.open("files\\foldericon.png")
folderIcon = folderIcon.resize((25,25))
folderIcon = ImageTk.PhotoImage(folderIcon)

previewText = Label(root, text="PREVIEW")
saveButton = Button(root, text="Save Screenshot", padx=10, pady=10, command=saveScreenshot)
setTitleLabel = Label(root, text="Chat Title:", padx=10, pady=10)
setTitleButton = Button(root, text="Set", padx=10, command=lambda: setTitle(currentCanvas))
titleEntry = Entry(root, width=20)
lb = Listbox(root, height=35, width=50)
addButton = Button(root, text="Add", padx=10, pady=10, command=addEntry)
deleteButton = Button(root, text="Delete", padx=10, pady=10, command=deleteEntry)
saveIndividualButton = Button(root, text="Save Selected Bubble", padx=10, pady=10, command=saveIndividual)
openDirectoryButton = Button(root, image=folderIcon, command=openDir)
openDirectoryButton.image = folderIcon
clearButton = Button(root, text="Clear", padx=10, pady=10, command=clear)

clearButton.config(state=DISABLED)
deleteButton.config(state=DISABLED)
saveButton.config(state=DISABLED)
saveIndividualButton.config(state=DISABLED)

imagePreviewWidget.grid(row=1, column=0, columnspan=2)
previewText.grid(row=0,column=0, columnspan=2)
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