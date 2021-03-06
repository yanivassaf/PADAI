import time
import pyautogui

# This is v0. It uses hard-coded positions and timers for all the buttons, so it's very fragile.

# v1 would take a screenshot of the screen and use image recognition to find the window and use
# hard-coded ratios to know the position.

# v2 would hopefully take screenshots and use image recognition to find the buttons, this would
# also eliminate the need for hard-coded timers

# v3 would hopefully add an abstraction layer that takes the screen and reads it all into memory
# then we should be able to navigate menus and such at a higher level.

# v4 may even use OCR, but probably images of all texts would suffice

focusPoint = (160, 20)
points = ((160, 445), 1.7, # Endless Corridors  should be 495
		  (160, 205), 2.2, # Endless Corridors 1/1
		  (160, 205), 1.7, # Chooose Friend
		  (160, 355), 1.7, # Select (confirm friend)
		  (160, 495), 5.2, # Enter game (wait a while for menu to close and game to open)
		  (160, 47),  1.2, # Mobizen Menu
		  (85, 65),   1.2, # Screenshot
		  (299, 80),  1.7, # Game Menu
		  (160, 395), 1.7, # Quit
		  (125, 375), 4.4) # Yes (wait a while for game to close and menu to open)

def distance(p1, p2):
	return (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2

def wait(seconds = .1):
	time.sleep(seconds)
	
def moveTo(point):
	pyautogui.moveTo(point[0], point[1])
	wait()
	
def click():
	pyautogui.mouseDown()
	wait(0.02)
	pyautogui.mouseUp()
	wait()

# Public
# Give focus to Mobizen
def setFocusToMobizen():
	pyautogui.moveTo(focusPoint)
	pyautogui.click()
	return focusPoint

# Public
# Loop through all point clicks.
def captureScreenshots():
	i = 0
	count = 0
	lastPoint = focusPoint
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
			
	logEnd(startTime, count)

# Log end of program
def logEnd(startTime, count):
	elapsedTime = (time.time() - startTime)
	print "%s Finished %d in %0.2f" % (time.strftime("%H:%M:%S"), count, elapsedTime)
	if count > 0:
		print "Average time: %0.2f" % (elapsedTime / count)

'''
# Screenshot code:
pyautogui.screenshot('my_screenshot.png')


# Show an image code:
cv2.imshow('image',image)
cv2.waitKey(0)
cv2.destroyWindow('image')
'''