import time
import wx

# Given that I currently use hard-coded pixels, then we need to find them. This is used for it.

# While true, listen for the mouse, and if mouse down, print and wait .2 secs
app = wx.App()
while True:
	if wx.GetMouseState().LeftIsDown():
		print wx.GetMousePosition()
		time.sleep(.2)
