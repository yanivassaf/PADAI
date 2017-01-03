import os
import numpy
import cv2
import sys

sys.path.append('../image processing/')

import processImage

screenshotsLocation = "C:\Users\Public\Documents\Rsupport\Mobizen"
croppedImageDirectory = "croppedScreenshots"
orbIconNames = ("icon_red", "icon_green", "icon_blue", "icon_yellow", "icon_purple", "icon_heart")
orbIcons = [cv2.imread(iconName+".png") for iconName in orbIconNames]

# Public
# Find all new screenshots
def cropNewImages(process = True):
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
			if not process or processImage.processImage(cropped, filename, orbIcons):	# If processing image succeeds
				outputPath = os.path.join(croppedImageDirectory, filename)
				cv2.imwrite(outputPath, cropped)		# Save croppedImage
				os.remove(path)							# Only delete it if success (for now)
			else:
				print "Unable to process image", filename

# Utility function if we want to reprocess everything. Shouldn't be done often.
def processAllCroppedImages():
	for (dirpath, dirnames, filenames) in os.walk(croppedImageDirectory):
		for filename in filenames:
			if not filename.endswith(".png"):
				continue
			
			processImage.processImage(cv2.imread(os.path.join(dirpath, filename)), filename, orbIcons)


if __name__ == '__main__':
	processAllCroppedImages()