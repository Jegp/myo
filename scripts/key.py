scriptTitle = "Keyboard left/right"
scriptDescription = "Click left/right keys on waves"

commandStart = 0
commandActive = False
lastCommandStart = 0
lastUnlocked = 0
isLocked = True

def onUnlock():
	global isLocked, lastCommandStart, lastUnlocked
	myo.unlock("hold")
	isLocked = False
	lastCommandStart = myo.getTimeMilliseconds()
	lastUnlocked = lastCommandStart

def onPeriodic():
	global commandStart, commandActive, lastCommandStart, isLocked, lastUnlocked
	if not isLocked:
		if (commandStart != 0):
			delta = myo.getTimeMilliseconds() - lastCommandStart
			if delta >= 290 and delta <= 410:
				myo.vibrate("medium")
			if delta >= 490 and delta <= 910:
				myo.vibrate("long")
			if delta >= 600:
				commandStart = 0
				myo.centerMousePosition()
		if commandActive == "fist" and commandStart == 0:
			myo.mouseMove(600 + myo.rotYaw() * 2000, 500 + myo.rotPitch() * 2000)
	
		if lastCommandStart > 0 and commandActive == False and\
			(myo.getTimeMilliseconds() - lastCommandStart > 2000 or \
			(myo.getTimeMilliseconds() - lastUnlocked > 1000 and\
			lastUnlocked > 0)):
			isLocked = True
			lastUnlocked = 0
			myo.notifyUserAction()
			print("locked")

def onPoseEdge(pose, edge):
	global commandStart, commandActive, lastCommandStart, isLocked, lastUnlocked

	if edge == 'on' and \
		isLocked and \
		pose == 'doubleTap' and \
		myo.getTimeMilliseconds() - lastCommandStart > 500:
		lastCommandStart = myo.getTimeMilliseconds()
		lastUnlocked = lastCommandStart
		isLocked = False
		myo.notifyUserAction()
		myo.notifyUserAction()
		print("unlocked")

	elif edge == 'on' and not isLocked: 
		lastCommandStart = myo.getTimeMilliseconds()
		print(pose, edge, isLocked)

		if pose != 'rest':
			lastUnlocked = 0
		if pose == 'doubleTap':
			myo.notifyUserAction()
			isLocked = True
			commandActive = False
			commandStart = 0
			print("locked")
		elif (pose == "waveOut"): # next slide
			myo.keyboard("right_arrow", "press", "")
		elif (pose == "waveIn"): # prev slide
			myo.keyboard("left_arrow", "press", "")
		elif (pose == "fist"): # toggle fist
			if commandActive == "fist":
				commandActive = False
				commandStart = 0
			elif commandActive != "fist":
				commandStart = lastCommandStart
				commandActive = "fist"

