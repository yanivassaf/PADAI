import numpy
import cv2

threshold = 0.92
colors = ("red", "green", "blue", "yellow", "purple", "heart")
box_colors = ((0,0,255), (0,255,0), (255,0,0), (0,255,255), (205,0,205), (255,100,255))

# Public
# To reduce computation time, we want to crop first, then try to process
def processImage(image, name, orbIcons):
	foundPositions = processImage.findOrbIcons(image, orbIcons)  # [[(x,y),(x,y),...],[(x,y),(x,y),...],...] 6 sublists, 1 for each color
	
	colorIndependent = reduce(lambda x,y:x+y, foundPositions)
	separateXandY = zip(*colorIndependent)
	cleanedUpPoints = [sorted(set(separateList)) for separateList in separateXandY]
	thresholds = [findThresholds(separateList) for separateList in cleanedUpPoints]
	
	correctPositions = [[thresholdPointLookup(point, thresholds) for point in sublist] for sublist in foundPositions]
	
	finalArr = [[-1] * (len(thresholds[1])+1) for i in range(len(thresholds[0])+1)]
	for i, sublist in enumerate(correctPositions):
		for x, y in sublist:
			finalArr[x][y] = i
	
	print finalArr
		
	cv2.imwrite('res.png',image)
		
	return True

# Takes an array of values, and returns which ones have the biggest difference from the ones before them.
# This assumes that we do not have any outlier points which could throw it off.
def findThresholds(arr):
	differences = numpy.diff(arr)
	cleanedUpDifferences = sorted(set(differences))
	secondDerivative = numpy.diff(cleanedUpDifferences)
	maxesOfSecondDerivative = max((v, i) for i, v in enumerate(secondDerivative))
	smallestThresholdDiff = cleanedUpDifferences[maxesOfSecondDerivative[1] + 1]
	thresholds = [arr[i+1] for i in range(len(differences)) if differences[i] >= smallestThresholdDiff]
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

# Template search and find all orb locations that match. This will have duplicates 1 pixel apart.
def findOrbIcons(image, orbIcons, drawRectangles = False):
	total = 0
	foundPositions = []
	for i in range(len(colors)):
		color = colors[i]
		icon = orbIcons[i]
		h, w = icon.shape[:-1]
		foundOfThisColor = []
		
		res = cv2.matchTemplate(image,icon,cv2.TM_CCOEFF_NORMED)
		loc = zip(*numpy.where( res >= threshold)[::-1])
		
		#print color, loc
		
		if drawRectangles:
			for pt in loc:
				cv2.rectangle(image, pt, (pt[0] + w, pt[1] + h), box_colors[i], 1)
		
		total += len(loc)
		foundPositions += [loc]
	
	#print "Found", total, "orbs"#, foundPositions
	return foundPositions

if __name__ == '__main__':
	processAllCroppedImages()