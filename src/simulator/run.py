import captureScreenshots
import processScreenshots

if __name__ == '__main__':
	captureScreenshots.setFocusToMobizen()
	captureScreenshots.captureScreenshots()
	processScreenshots.cropNewImages()