import time
import numpy
import wx
import pyautogui
import cv2
import os

# This is v0. It uses hard-coded positions and timers for all the buttons, so it's very fragile.

# v1 would take a screenshot of the screen and use image recognition to find the window and use
# hard-coded ratios to know the position.

# v2 would hopefully take screenshots and use image recognition to find the buttons, this would
# also eliminate the need for hard-coded timers

# v3 would hopefully add an abstraction layer that takes the screen and reads it all into memory
# then we should be able to navigate menus and such at a higher level.

# v4 may even use OCR, but probably images of all texts would suffice


threshold = 0.92
focus = (160, 20)
points = ((160, 495), 1.7, # Endless Corridors
		  (160, 205), 2.2, # Endless Corridors 1/1
		  (160, 205), 1.7, # Chooose Friend
		  (160, 355), 1.7, # Select (confirm friend)
		  (160, 495), 5.2, # Enter game (wait a while for menu to close and game to open)
		  (160, 47),  1.2, # Mobizen Menu
		  (85, 65),   1.2, # Screenshot
		  (299, 80),  1.7, # Game Menu
		  (160, 395), 1.7, # Quit
		  (125, 375), 4.4) # Yes (wait a while for game to close and menu to open)
screenshotsLocation = "C:\Users\Public\Documents\Rsupport\Mobizen"
croppedImageDirectory = "croppedScreenshots"
colors = ("red", "green", "blue", "yellow", "purple", "heart")
box_colors = ((0,0,255), (0,255,0), (255,0,0), (0,255,255), (205,0,205), (255,100,255))
orbIconNames = ("icon_red", "icon_green", "icon_blue", "icon_yellow", "icon_purple", "icon_heart")
orbIcons = [cv2.imread(iconName+".png") for iconName in orbIconNames]

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
def setFocusToMobizen():
	pyautogui.moveTo(focus)
	pyautogui.click()
	return focus

# Loop through all point clicks.
def captureScreenshots():
	i = 0
	count = 0
	lastPoint = setFocusToMobizen()
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
		
# Find all new screenshots
def cropNewImages():
	f = []
	
	# Make cropped image directory if necessary
	if not os.path.exists(croppedImageDirectory):
		os.makedirs(croppedImageDirectory)
	
	# Loop through new iamges
	for (dirpath, dirnames, filenames) in os.walk(screenshotsLocation):
		for filename in filenames:
			if not filename.endswith(".png"): # If it is unexpected, ignore it
				continue
			
			path = os.path.join(dirpath, filename)
			img = cv2.imread(path)						# Read image
			cropped = img[405:705, 18:374]				# Crop image
			if processCroppedImage(cropped, filename):	# If processing image succeeds
				outputPath = os.path.join(croppedImageDirectory, filename)
				cv2.imwrite(outputPath, cropped)		# Save croppedImage
				os.remove(path)							# Only delete it if success (for now)
			else:
				print "Unable to process image", filename
			
# Template search and find all orb locations that match. This will have duplicates 1 pixel apart.
def findOrbIcons(image):
	total = 0
	foundPositions = []
	for i in range(len(colors)):
		color = colors[i]
		icon = orbIcons[i]
		h, w = icon.shape[:-1]
		foundOfThisColor = []
		
		res = cv2.matchTemplate(image,icon,cv2.TM_CCOEFF_NORMED)
		loc = zip(*numpy.where( res >= threshold)[::-1])
		
#		print color, len(loc), loc
#		for pt in loc:
#			print pt, res[pt[1]][pt[0]]
#			cv2.rectangle(image, pt, (pt[0] + w, pt[1] + h), box_colors[i], 1)
		
		total += len(loc)
		foundPositions += [loc]
	
	#print "Found", total, "orbs"#, foundPositions
	return foundPositions
	
# Takes an array of values, and returns which ones have the biggest difference from the ones before them.
# This assumes that we do not have any outlier points which could throw it off.
def findThresholds(arr):
	#print "Array:", arr
	differences = numpy.diff(arr)
	#print "Differences:", differences
	cleanedUpDifferences = sorted(set(differences))
	#print "Differences cleaned up:", cleanedUpDifferences
	secondDerivative = numpy.diff(cleanedUpDifferences)
	#print "Second derivative:", secondDerivative
	maxesOfSecondDerivative = max((v, i) for i, v in enumerate(secondDerivative))
	#print "Max of second derivative:", maxesOfSecondDerivative[0], "at index:", maxesOfSecondDerivative[1]
	smallestThresholdDiff = cleanedUpDifferences[maxesOfSecondDerivative[1] + 1]
	#print "Smallest threshold diff:", smallestThresholdDiff
	thresholds = [arr[i+1] for i in range(len(differences)) if differences[i] >= smallestThresholdDiff]
	#print "Thresholds:", thresholds
	return thresholds
	
# Converts a point to final index
def thresholdPointLookup(point, thresholds):
	return (thresholdLookup(point[0], thresholds[0]), thresholdLookup(point[1], thresholds[1]))

# Convert a value to final index, given the thresholds
def thresholdLookup(value, thresholds):
	position = 0
	while position < len(thresholds) and value >= thresholds[position]:
		position += 1
	return position
			
# To reduce computation time, we want to crop first, then try to process
def processCroppedImage(image, name):
	foundPositions = findOrbIcons(image)  # [[(x,y),(x,y),...],[(x,y),(x,y),...],...] 6 sublists, 1 for each color
	
	colorIndependent = reduce(lambda x,y:x+y, foundPositions) # [(x,y),(x,y),...]
	#print colorIndependent
	separateXandY = zip(*colorIndependent)
	#print separateXandY
	cleanedUpPoints = [sorted(set(separateList)) for separateList in separateXandY]
	#print cleanedUpPoints
	thresholds = [findThresholds(separateList) for separateList in cleanedUpPoints]
	#print thresholds
	
	correctPositions = [[thresholdPointLookup(point, thresholds) for point in sublist] for sublist in foundPositions]
	#print foundPositions
	#print correctPositions
	
	finalArr = [[-1] * (len(thresholds[1])+1) for i in range(len(thresholds[0])+1)]
	for i, sublist in enumerate(correctPositions):
		for x, y in sublist:
			finalArr[x][y] = i
	
	print finalArr
	
	'''
	cv2.imshow('image',image)
	cv2.waitKey(0)
	cv2.destroyWindow('image')
	'''
		
	cv2.imwrite('res.png',image)
		
	return True
		

# Utility function if we want to reprocess everything. Shouldn't be done often.
def processAllCroppedImages():
	for (dirpath, dirnames, filenames) in os.walk(croppedImageDirectory):
		for filename in filenames:
			if not filename.endswith(".png"):
				continue
			
			processCroppedImage(cv2.imread(os.path.join(dirpath, filename)), filename)


if __name__ == '__main__':
	#setFocusToMobizen()
	#captureScreenshots()
	cropNewImages()
	processAllCroppedImages()
	
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
'''