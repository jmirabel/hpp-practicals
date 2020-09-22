from __future__ import print_function
from hpp.corbaserver.ur5 import Robot
from hpp.corbaserver import ProblemSolver, newProblem
from hpp.gepetto import ViewerFactory, PathPlayer
import numpy as np

newProblem()
robot = Robot ('ur5')
ps = ProblemSolver (robot)

vf = ViewerFactory (ps)
r = vf.createViewer ()

q1 = [0, -1.57, 1.57, 0, 0, 0]; q2 = [0.2, -1.57, -1.8, 0, 0.8, 0]
q3 = [3, -1.57, -1.8, 0, 0.8, 0]

#create target object
gui = r.client.gui
scene = "target"
r.client.gui.createScene(scene)
boxname = scene+"/t0"
target = [0,0,0,0,0,0,1]
gui.addBox(boxname,0.03,0.03,0.03, [1,1,1,1])
gui.applyConfiguration(boxname,target)
gui.addToGroup(scene,r.sceneName)
gui.refresh()

# Create the forward kinematic function
ps.createPositionConstraint("pos_cons", 'wrist_3_joint', '', [0,0,0], [0,0,0], [True,True,True])
fk = ps.client.problem.getConstraint("pos_cons").function()

import time

#call to update target position
def updateTarget(x,y,z):
	global gui
	global com
	global target
	target[0:3] = [x,y,z]
	gui.applyConfiguration(boxname,target)
	gui.refresh()

r (q2)

from numpy import array, transpose
from numpy.linalg import pinv, norm
from time import sleep

def ik(x,y,z):
	#set visual marker target
	updateTarget(x,y,z)

        # Compute the position of the end-effector as follow
        pos = np.array(fk.value(q1))
        # and the jacobian as follow
        Jacobian = np.array(fk.jacobian(q1))

	print ("TODO: implement inverse kinematics")
		
ik(-0.42, 0.03, 0.8)
ik(0.42, 0.03, 0.8)
ik(1, 0.03, 0.8)
	
	

