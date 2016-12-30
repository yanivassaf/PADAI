import time
import numpy
import wx
import pyautogui
import cv2

# This is v0. It uses hard-coded positions and timers for all the buttons, so it's very fragile.
# v1 would take a screenshot of the screen and use image recognition to find the window and use
# hard-coded ratios to know the position.
# v2 would hopefully take screenshots and use image recognition to find the buttons, this would
# also eliminate the need for hard-coded timers
# v3 would hopefully add an abstraction layer that takes the screen and reads it all into memory
# then we should be able to navigate menus and such at a higher level.
# v4 may even use OCR, but probably images of all texts would suffice
focus = (160, 20)
points = ((160, 495), 1.5, # Endless Corridors
		  (160, 205), 2.0, # Endless Corridors 1/1
		  (160, 205), 1.5, # Chooose Friend
		  (160, 355), 1.5, # Select (confirm friend)
		  (160, 495), 5.0, # Enter game (wait a while for menu to close and game to open)
		  (160, 47),  1.0, # Mobizen Menu
		  (85, 65),   1.0, # Screenshot
		  (299, 80),  1.5, # Game Menu
		  (160, 395), 1.5, # Quit
		  (125, 375), 4.2) # Yes (wait a while for game to close and menu to open)

def distance(p1, p2):
	return (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2

def wait(seconds = .1):
	time.sleep(seconds)
	
def moveTo(point):
	pyautogui.moveTo(point[0], point[1])
	wait()
	
def click():
	pyautogui.mouseDown()
	wait()
	pyautogui.mouseUp()
	wait()

# Give focus to Mobizen
lastPoint = focus
pyautogui.moveTo(lastPoint)
pyautogui.click()

i = 0
count = 0
startTime = prevTime = time.time()

while distance(lastPoint, pyautogui.position()) < 100:
	# Do next click
	lastPoint = points[i]
	moveTo(lastPoint)
	click()
	wait(points[i+1])
	i = (i + 2) % len(points)
	
	if i == 0:
		# Log successful screenshot
		now = time.time()
		count = count + 1
		print "%s Screenshot #%d, elapsedTime: %0.2f" % (time.strftime("%H:%M:%S"), count, now - prevTime)
		prevTime = now

# Log end of program
now = time.time()
elapsedTime = (now - startTime)
print "%s Finished %d in %0.2f" % (time.strftime("%H:%M:%S"), count, elapsedTime)
if count > 0:
	print "Average time: %0.2f" % (elapsedTime / count)

	
	
'''
# Screenshot code:
wx.App()  # Need to create an App instance before doing anything
screen = wx.ScreenDC()
size = screen.GetSize()
bmp = wx.EmptyBitmap(size[0], size[1])
mem = wx.MemoryDC(bmp)
mem.Blit(0, 0, size[0], size[1], screen, 0, 0)
del mem  # Release bitmap
bmp.SaveFile('screenshot.png', wx.BITMAP_TYPE_PNG)