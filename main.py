from imageProcessing import createBubble, loadAvatar
import os

if "output" not in os.listdir():
	os.mkdir(output)

# createBubble(loadAvatar("files\\austinavy.jpg"), "duskblades are so fucking cute")
avatar = loadAvatar(input("Path to avatar:\n"))
text = input("Input your text:\n")
side = input("Position of bubble left or right?\n")

createBubble(avatar, text, side)