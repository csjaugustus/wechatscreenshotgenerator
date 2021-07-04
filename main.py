from imageProcessing import createBubble, loadAvatar, get_concat_v, drawTitle
import os
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk

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
	
def editEntry():
	pass

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

		#update preview img
		img = entries[0]
		if len(entries) > 1:
			for i in range(1, len(entries)):
				img = get_concat_v(img, entries[i])
		if img.size[1] <= maxChatHeight:
			currentCanvas.paste(img, (0,113))
		else:
			popupMessage("Error", "Chat content too long for one screenshot.")
			return

		lb.insert(END, text)

		updatePreview()

	def selectAvatar(x):
		e1.config(state=NORMAL)
		e1.delete(0, END)
		e1.insert(0, x)
		e1.config(state=DISABLED)

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
	pass

def saveScreenshot():
	currentCanvas.save("output\\screenshot.png")

def setTitle(currentCanvas):
	title = titleEntry.get()
	currentCanvas = drawTitle(currentCanvas, title)
	updatePreview()
	

maxChatHeight = 1684
entries = []

if "output" not in os.listdir():
	os.mkdir(output)

root = Tk()
root.title("WeChat Screenshot Generator")

currentCanvas = Image.open("files\\blankScreenshot.png")
w, h = currentCanvas.size
imagePreview = currentCanvas.resize((round(w/3), round(h/3)))
imagePreview = ImageTk.PhotoImage(imagePreview)
imagePreviewWidget = Label(root, image=imagePreview)

previewText = Label(root, text="Preview:")
saveButton = Button(root, text="Save", padx=10, pady=10, command=saveScreenshot)
setTitleLabel = Label(root, text="Set title:", padx=10, pady=10)
setTitleButton = Button(root, text="Set Title", padx=10, pady=10, command=lambda: setTitle(currentCanvas))
titleEntry = Entry(root, width=30)
lb = Listbox(root, height=35, width=40)
addButton = Button(root, text="Add", padx=10, pady=10, command=addEntry)
deleteButton = Button(root, text="Delete", padx=10, pady=10, command=deleteEntry)
editButton = Button(root, text="Edit", padx=10, pady=10, command=editEntry)

imagePreviewWidget.grid(row=1, column=0)
previewText.grid(row=0,column=0)
setTitleLabel.grid(row=0, column=1)
titleEntry.grid(row=0,column=2)
setTitleButton.grid(row=0, column=3)
lb.grid(row=1,column=1, columnspan=3)
saveButton.grid(row=2,column=0)
addButton.grid(row=2, column=1)
deleteButton.grid(row=2,column=2)
editButton.grid(row=2,column=3)


root.mainloop()