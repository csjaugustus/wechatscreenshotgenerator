from PIL import Image, ImageDraw, ImageFont
import re
import os


def get_concat_h(im1, im2):
    dst = Image.new('RGB', (im1.width + im2.width, max(im1.height,im2.height)), color=(237,237,237))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width, 0))
    return dst

def get_concat_v(im1, im2):
    dst = Image.new('RGB', (max(im1.width, im2.width), im1.height + im2.height), color=(237,237,237))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (0, im1.height))
    return dst

def sortText(text):
	seq = []

	pattern = re.compile("[\\dA-Za-z\\s.,\"$%!?:()-\u2014;\u00e9]+")
	matches = pattern.findall(text)

	current_lang = ""

	while True:
		if any(text.startswith(match) for match in matches):
			current_lang = "en"
			for match in matches:
				if text.startswith(match):
					seq.append(match)
					text = text.lstrip(match)
		else:
			if current_lang == "cn":
				seq[-1] = seq[-1] + text[0]
				text = text[1:]
			else:
				current_lang = "cn"
				seq.append(text[0])
				text = text[1:]
		if not text:
			break

	return seq	

def getTextSize(text, title=False):
	if not text:
		return (0, 0)

	pattern = re.compile("[\\dA-Za-z\\s.,\"$%!?:()-\u2014;\u00e9]+")
	w, h = 0, 0
	seq = sortText(text)

	if pattern.findall(seq[0]): #first element is not chinese
		if title:
			ft = enTitleFont

			for el in seq:
				tw, th = draw.textsize(el, font=ft)
				w += tw
				if th > h:
					h = th
				if ft == enTitleFont:
					ft = cnTitleFont
				else:
					ft = enTitleFont

		else:
			ft = enTextFont

			for el in seq:
				tw, th = draw.textsize(el, font=ft)
				w += tw
				if th > h:
					h = th
				if ft == enTextFont:
					ft = cnTextFont
				else:
					ft = enTextFont
	else:
		if title:
			ft = cnTitleFont

			for el in seq:
				tw, th = draw.textsize(el, font=ft)
				w += tw
				if th > h:
					h = th
				if ft == enTitleFont:
					ft = cnTitleFont
				else:
					ft = enTitleFont

		else:
			ft = cnTextFont

			for el in seq:
				tw, th = draw.textsize(el, font=ft)
				w += tw
				if th > h:
					h = th
				if ft == enTextFont:
					ft = cnTextFont
				else:
					ft = enTextFont

	return (w, h)

def drawText(imgDrawObj, xcoord, ycoord, text, fill, title=False):
	draw = imgDrawObj
	pattern = re.compile("[\\dA-Za-z\\s.,\"$%!?:()-\u2014;\u00e9]+")
	seq = sortText(text)

	if pattern.findall(seq[0]): #first element is not chinese
		if title:
			ft = enTitleFont

			for el in seq:
				draw.text((xcoord, ycoord), el, font=ft, fill=fill)
				tw, th = draw.textsize(el, font=ft)
				if ft == enTitleFont:
					ft = cnTitleFont
				else:
					ft = enTitleFont
				xcoord += tw
		else:
			ft = enTextFont

			for el in seq:
				draw.text((xcoord, ycoord), el, font=ft, fill=fill)
				tw, th = draw.textsize(el, font=ft)
				if ft == enTextFont:
					ft = cnTextFont
				else:
					ft = enTextFont
				xcoord += tw
	else:
		if title:
			ft = cnTitleFont

			for el in seq:
				draw.text((xcoord, ycoord), el, font=ft, fill=fill)
				tw, th = draw.textsize(el, font=ft)
				if ft == enTitleFont:
					ft = cnTitleFont
				else:
					ft = enTitleFont
				xcoord += tw
		else:
			ft = cnTextFont

			for el in seq:
				draw.text((xcoord, ycoord), el, font=ft, fill=fill)
				tw, th = draw.textsize(el, font=ft)
				if ft == enTextFont:
					ft = cnTextFont
				else:
					ft = enTextFont
				xcoord += tw

def createBubble(avatar, text, side):
	def breakWord(word):
		lst = []
		while word:
			indx = 0
			for i in range(1, len(word)+1):
				part = word[:i]
				width = getTextSize(part)[0]
				if width <= maxTextWidth:
					indx = i
				else:
					break
			lst.append(word[:indx])
			word = word[indx:]
		return lst

	#split text into lines
	lines = []
	temp = text.split()
	splitText = []
	for word in temp:
		if getTextSize(word)[0] <= maxTextWidth:
			splitText.append(word)
		else:
			splitText += breakWord(word)

	indx = 0
	while splitText:
		for i in range(1,len(splitText)+1):
			currentLine = " ".join(splitText[:i])
			if getTextSize(currentLine)[0] <= maxTextWidth:
				indx = i
			else:
				break
		line = " ".join(splitText[:indx])
		splitText = splitText[indx:]
		lines.append(line)

	textHeight = 0
	for l in lines:
		th = getTextSize(l)[1]
		textHeight += th
	h = 2 * topMargin + 2 * bubbleTopMargin + (len(lines)-1) * bubbleLineMargin + textHeight

	#round avatar mask
	corner = Image.new('RGBA', (10,10), (0,0,0,0))
	cornerDraw = ImageDraw.Draw(corner)
	cornerDraw.pieslice((0,0, 20, 20), 180, 270, fill="black")
	sq = Image.new('RGBA', (86,86), "black")
	sq.paste(corner, (0,0))
	sq.paste(corner.rotate(90), (0, 86-10))
	sq.paste(corner.rotate(180), (86-10, 86-10))
	sq.paste(corner.rotate(270), (86-10, 0))

	userCanvas = Image.new('RGB', (w, h), color=(237,237,237))
	if side == "left":
		userCanvas.paste(avatar, (sideMargin, topMargin), mask=sq)
	elif side == "right":
		userCanvas.paste(avatar, (w-sideMargin-86, topMargin), mask=sq)
	
	longestLineLength = max(getTextSize(l)[0] for l in lines)
	if longestLineLength <= 535:
		bubbleWidth = longestLineLength + 2 * 30
		bubbleSideMargin = 30
	else:
		bubbleWidth = fixedBubbleWidth
		bubbleSideMargin = (fixedBubbleWidth - max(getTextSize(l)[0] for l in lines))/2

	bubbleHeight = 2 * bubbleTopMargin + (len(lines)-1) * bubbleLineMargin + textHeight

	#round bubble corners
	bubbleMask = Image.new('RGBA', (bubbleWidth, bubbleHeight), "black")
	bubbleMask.paste(corner, (0,0))
	bubbleMask.paste(corner.rotate(90), (0, bubbleHeight-10))
	bubbleMask.paste(corner.rotate(180), (bubbleWidth-10, bubbleHeight-10))
	bubbleMask.paste(corner.rotate(270), (bubbleWidth-10, 0))

	if side == "left":
		bubbleColour = (255,255,255)
	elif side == "right":
		bubbleColour = (151, 236, 106)
	bubble = Image.new('RGB', (bubbleWidth, bubbleHeight), color=bubbleColour)
	bubbleCanvas = Image.new('RGB', (bubbleWidth, bubbleHeight), color=(237,237,237))
	bubbleCanvas.paste(bubble, (0,0), mask=bubbleMask)

	bubbleDraw = ImageDraw.Draw(bubbleCanvas)
	
	yincrement = 0

	for l in lines:
		drawText(bubbleDraw, bubbleSideMargin, bubbleTopMargin+yincrement, l, "#1c1c1c")
		yincrement += bubbleLineMargin + getTextSize(l)[1]

	if side == "left":
		speechBubble = get_concat_h(whitearrow, bubbleCanvas)
		userCanvas.paste(speechBubble, (sideMargin+86, topMargin))
	elif side == "right":
		speechBubble = get_concat_h(bubbleCanvas, greenarrow)
		arrowWidth = greenarrow.size[0]
		userCanvas.paste(speechBubble, (w-bubbleWidth-2*arrowWidth-86, topMargin))

	userCanvas.save('output\\usercanvas.png')
	return userCanvas

def drawTitle(canvas, title):
	canvas.paste(titlebar, (0,0))
	if title:
		draw = ImageDraw.Draw(canvas)
		tw, th = getTextSize(title, title=True)
		drawText(draw, (w-tw)/2, (113-th)/2, title, "#1c1c1c", title=True)
	return canvas

def loadAvatar(avypath):
	avatar = Image.open(avypath)
	avatar = avatar.resize((86,86))
	return avatar

#fonts
enTitleFont = ImageFont.truetype('files\\Roboto-Medium-12.ttf', 36)
enTextFont = ImageFont.truetype('files\\Roboto-Regular-14.ttf', 36)
cnTitleFont = ImageFont.truetype('files\\SourceHanSans-Medium.otf', 38)
cnTextFont = ImageFont.truetype('files\\SourceHanSans-Normal.otf', 38)

#constants
w, h = 864, 1920
topMargin = 14
sideMargin = 25
fixedBubbleWidth = 595
maxTextWidth = fixedBubbleWidth - 50
bubbleTopMargin = 25
bubbleLineMargin = 20

#images
titlebar = Image.open('files\\chattitle.png')
inputbox = Image.open('files\\inputbox.png')
whitearrow = Image.open('files\\speechbubblewhitearrow.png')
greenarrow = Image.open('files\\speechbubblegreenarrow.png')

#main canvas
canvas = Image.new('RGB', (w, h), color=(237,237,237))
canvas.paste(titlebar, (0,0))
canvas.paste(inputbox, (0, 1797))
draw = ImageDraw.Draw(canvas)

