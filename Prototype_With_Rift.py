""" 
Welcome to our art gallery! Please walk around and visit each of the paintings at
your own pace.
""" 

import viz
import vizact
import viztask
import vizcam
import random

viz.setMultiSample(4)
viz.fov(40)
viz.go()

# Setup keyboard/mouse tracker
tracker = vizcam.addWalkNavigate(moveScale=2.0)
tracker.setPosition([0,1.8,0])
viz.link(tracker,viz.MainView)
viz.mouse.setVisible(False)
viz.collision(viz.ON)

viz.MainView.setPosition([4, 0, 2])
gallery = viz.addChild('gallery.osgb')



#-----------Info panel set up--------------------
import vizinfo
#Add info panel to display messages to participant
instructions = vizinfo.InfoPanel(icon=False,key=None)
#------------------------------------------------

#-----------Sensor creation----------------------
import vizproximity
target = vizproximity.Target(viz.MainView)

viewPath = []
inTime = 0

MainViewApproaches = 0
sensor1 = vizproximity.Sensor(vizproximity.RectangleArea([3,1],center=[-4,0.375]), None )
sensor2 = vizproximity.Sensor(vizproximity.RectangleArea([2.25, 2.25], center=[-4, 2.5]), None)
sensor3 = vizproximity.Sensor(vizproximity.RectangleArea([3, 1], center=[-4, 4.75]), None)
sensor4 = vizproximity.Sensor(vizproximity.RectangleArea([2.25, 1.5],center=[-4, 6.75]), None)
sensor5 = vizproximity.Sensor(vizproximity.CircleArea(0.75, center=[2, 7.5]), None)
sensor6 = vizproximity.Sensor(vizproximity.RectangleArea([2.5, 2.5], center=[0, 7.5]), None)
sensor7 = vizproximity.Sensor(vizproximity.CircleArea(0.75, center=[-2, 7.5]), None)
sensor8 = vizproximity.Sensor(vizproximity.RectangleArea([2.25, 1.5], center=[4, 6.75]), None)
sensor9 = vizproximity.Sensor(vizproximity.RectangleArea([3, 1], center=[4, 4.75]), None)
sensor10 = vizproximity.Sensor(vizproximity.RectangleArea([2.5, 2.25], center=[4, 2.5]), None)
sensor11 = vizproximity.Sensor( vizproximity.RectangleArea([4.25,1],center=[4,0.375]), None )

sensorList = [sensor1, sensor2, sensor3, sensor4, sensor5, sensor6, sensor7, sensor8, sensor9, sensor10, sensor11]
#------------------------------------------------

#-----------Manager creation & set up------------
manager = vizproximity.Manager()
avatarManager = vizproximity.Manager()
#Toggle debug shapes with keypress
vizact.onkeydown('p',manager.setDebug, viz.TOGGLE)
vizact.onkeydown('p', avatarManager.setDebug, viz.TOGGLE)
manager.addTarget(target)

#-----------Avatar's position creation & organization-----
positions = []
positions.append([-3, 0, 0.375])
positions.append([-3, 0, 2.5])
positions.append([-3, 0, 4.75])
positions.append([-3, 0, 6.75])
positions.append([-2, 0, 7.5])
positions.append([3, 0, 6.75])
positions.append([2, 0, 7.5])
positions.append([0, 0, 7])
positions.append([3, 0, 4.75])
positions.append([3, 0, 2.5])
positions.append([2, 0, 0.375])
#------------------------------------------------

#------------Avatar creation---------------------
avatars = []

for x in range(0,3):
	a = viz.addChild('vcc_male.cfg')
	a.state(1)
	a.setPosition(random.choice(positions))
	avatars.append(a)
#------------------------------------------------

for a in avatars:
	avaTarget = vizproximity.Target(a)
	# need to add sensors to each of the avatars
	avatarSensor = vizproximity.Sensor(vizproximity.Box([2, 4, 2]), source = a)
	avatarManager.addSensor(avatarSensor)
	manager.addTarget(avaTarget)
	
avatarManager.addTarget(target)

for s in sensorList:
	manager.addSensor(s)
#------------------------------------------------

#-----------Random movement of avatars-----------
def moveAvatars() :
	for a in avatars:
		walk = vizact.walkTo(random.choice(positions))
		a.runAction(walk)
#------------------------------------------------
	
vizact.onkeydown(' ', moveAvatars)

#---------Move an avatar every 8 seconds----------

curAvatar = random.choice(avatars)

def moveAvatar() :
	global curAvatar
	
	a = random.choice(avatars)
	#so a different avatar is choosen each time
	while(a == curAvatar):
		a = random.choice(avatars)

	curAvatar = a
	walk = vizact.walkTo(random.choice(positions))
	a.runAction(walk)

myTimerAction = vizact.ontimer(4, moveAvatar)
vizact.onkeydown('x', myTimerAction.setEnabled, 0)

#------------Analytics--------------------------

global startTime
analytics = []
cur_dict = {}

def writeToFile():
	global analytics
	global MainViewApproaches
	global startTime
	
	file = open('analytics_file', 'w')
	file.write("Analytics Data:\n\n")
	cur_dict = {"Approaches": str(MainViewApproaches)}
	analytics.append(cur_dict)
	cur_dict = {}
	cur_dict = {"Total Time ": (viz.getFrameTime()-startTime)}
	analytics.append(cur_dict)
	file.writelines(["%s\n" % dict  for dict in analytics])
	
	
	
def endOfProgram():
	writeToFile()

vizact.onkeydown('k', endOfProgram)

#-----------Proximity methods--------------------
def ProximityWork(e):
	global inTime
	global cur_dict
	
	viewPath.append(viz.MainView.getPosition())
	bodies = manager.getActiveTargets(e.sensor)
	inTime = viz.getFrameTime()
	print "Body count in sensor", len(bodies)
	cur_dict.update({"Body_Count": len(bodies)})

def EnterProximity(e):
	"""@args vizproximity.ProximityEvent()"""
	global inTime
	global cur_dict
	
	
	
	if e.sensor == sensor1:
		if (sensor1 in manager.getSensorsContainingTarget(target)):
			instructions.visible(viz.ON)
			instructions.setText('Don Quixote - Pablo Picasso')
			ProximityWork(e)
			cur_dict.update({"Painting": 'Don Quixote - Pablo Picasso'})
	
	elif e.sensor == sensor2:
		if (sensor2 in manager.getSensorsContainingTarget(target)):
			instructions.visible(viz.ON)
			instructions.setText('The Persistence of Memory - Salvador Dali')
			ProximityWork(e)
			cur_dict.update({"Painting": 'The Persistence of Memory - Salvador Dali'})
		
	elif e.sensor == sensor3:
		if (sensor3 in manager.getSensorsContainingTarget(target)):
			instructions.visible(viz.ON)
			instructions.setText('Self-Portrait of Vincent Van Gogh')
			ProximityWork(e)
			cur_dict.update({"Painting": 'Self-Portrait of Vincent Van Gogh'})
		
	elif e.sensor == sensor4:
		if (sensor4 in manager.getSensorsContainingTarget(target)):
			instructions.visible(viz.ON)
			instructions.setText('A Twilight Venice - Claude Monet')
			ProximityWork(e)
			cur_dict.update({"Painting": 'A Twilight Venice - Claude Monet'})
		
	elif e.sensor == sensor5:
		if (sensor5 in manager.getSensorsContainingTarget(target)):
			instructions.visible(viz.ON)
			instructions.setText('Best Friends - Keith Haring')
			ProximityWork(e)
			cur_dict.update({"Painting": 'Best Friends - Keith Haring'})
		
	elif e.sensor == sensor6:
		if (sensor6 in manager.getSensorsContainingTarget(target)):
			instructions.visible(viz.ON)
			instructions.setText('Starry Night - Vincent Vango')
			ProximityWork(e)
			cur_dict.update({"Painting": 'Starry Night - Vincent Vango'})
		
	elif e.sensor == sensor7:
		if (sensor7 in manager.getSensorsContainingTarget(target)):
			instructions.visible(viz.ON)
			instructions.setText('The Scream - Edvard Munch')
			ProximityWork(e)
			cur_dict.update({"Painting": 'The Scream - Edvard Munch'})
		
	elif e.sensor == sensor8:
		if (sensor8 in manager.getSensorsContainingTarget(target)):
			instructions.visible(viz.ON)
			instructions.setText('Mona Lisa - Leonardo Da Vinci')
			ProximityWork(e)
			cur_dict.update({"Painting": 'Mona Lisa - Leonardo Da Vinci'})
		
	elif e.sensor == sensor9:
		if (sensor9 in manager.getSensorsContainingTarget(target)):
			instructions.visible(viz.ON)
			instructions.setText('Campbells Soup - Andy Warhol')
			ProximityWork(e)
			cur_dict.update({"Painting": 'Campbells Soup - Andy Warhol'})
		
	elif e.sensor == sensor10:
		if (sensor10 in manager.getSensorsContainingTarget(target)):
			instructions.visible(viz.ON)
			instructions.setText('The Birth of Venus - Sandro Botticelli')
			ProximityWork(e)
			cur_dict.update({"Painting": 'The Birth of Venus - Sandro Botticelli'})
		
	elif e.sensor == sensor11:
		if (sensor11 in manager.getSensorsContainingTarget(target)):
			instructions.visible(viz.ON)
			instructions.setText('The Son of Man - Rene Magritte')
			ProximityWork(e)
			cur_dict.update({"Painting": 'The Son of Man - Rene Magritte'})
		
def ExitProximity(e):
	"""@args vizproximity.ProximityEvent()"""
	global cur_dict
	global analytics
	
	
	if (e.target is target):
		instructions.visible(viz.OFF)
		time = (viz.getFrameTime() - inTime)
		print("Time spent in sensor: %.2f seconds" % time)
		cur_dict.update({"Time":time})
		
		#Analytics
		analytics.append(cur_dict)
		cur_dict = {}

manager.onEnter(None,EnterProximity)
manager.onExit(None,ExitProximity)
#------------------------------------------------
def EnterAvatarProximity(e):
	global cur_dict
	
	newPosition = viz.MainView.getPosition()
	newPosition[1] = newPosition[1]-1.8
	e.sensor.getSourceObject().lookAt(newPosition, 0, 0)
	e.sensor.getSourceObject().state(6)
	global MainViewApproaches
	MainViewApproaches += 1
	print "Approaches: " + str(MainViewApproaches)
		
def ExitAvatarProximity(e):
	e.sensor.getSourceObject().state(1)
	
avatarManager.onEnter(None, EnterAvatarProximity)
avatarManager.onExit(None, ExitAvatarProximity)

#------------------------------------------------
def main():
	moveAvatars()
	global startTime
	startTime = viz.getFrameTime()

if __name__ == "__main__":
	main()