from imageProcessing import createBubble, loadAvatar
import os
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk

def editEntry():
	pass

def addEntry():
	def confirm():
		print(var.get())

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
		if c == 3:
			c = 0
			r += 1

	l1 = Label(addWindow, text="Avatar Selected:", padx=10)
	e1 = Entry(addWindow, width=20)
	l1.grid(row=0, column=4)
	e1.grid(row=0, column=5)
	e1.config(state=DISABLED)

	l2 = Label(addWindow, text="Text:", padx=10)
	e2 = Entry(addWindow, width=20)
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
	pass


entries = {}

if "output" not in os.listdir():
	os.mkdir(output)

root = Tk()
root.title("WeChat Screenshot Generator")

imagePreview = Image.open("files\\blankScreenshot.png")
w, h = imagePreview.size
imagePreview = imagePreview.resize((round(w/3), round(h/3)))
imagePreview = ImageTk.PhotoImage(imagePreview)
imagePreviewWidget = Label(root, image=imagePreview)

previewText = Label(root, text="Preview:")
saveButton = Button(root, text="Save", padx=10, pady=10, command=saveScreenshot)
lb = Listbox(root, height=35, width=40)
addButton = Button(root, text="Add", padx=10, pady=10, command=addEntry)
deleteButton = Button(root, text="Delete", padx=10, pady=10, command=deleteEntry)
editButton = Button(root, text="Edit", padx=10, pady=10, command=editEntry)

imagePreviewWidget.grid(row=1, column=0)
previewText.grid(row=0,column=0)
lb.grid(row=1,column=1, columnspan=3)
saveButton.grid(row=2,column=0)
addButton.grid(row=2, column=1)
deleteButton.grid(row=2,column=2)
editButton.grid(row=2,column=3)


root.mainloop()

# # createBubble(loadAvatar("files\\austinavy.jpg"), "duskblades are so fucking cute")
# avatar = loadAvatar(input("Path to avatar:\n"))
# text = input("Input your text:\n")
# side = input("Position of bubble left or right?\n")

# createBubble(avatar, text, side)