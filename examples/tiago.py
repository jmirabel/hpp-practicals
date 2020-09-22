from hpp.corbaserver import Robot, loadServerPlugin, createContext, newProblem, ProblemSolver
from hpp.gepetto import ViewerFactory
import sys, argparse

newProblem()

# parse arguments
Robot.urdfFilename = "package://tiago_data/robots/tiago_pal_hey5.urdf"
Robot.srdfFilename = "package://tiago_data/srdf/pal_hey5_gripper.srdf"

class Driller:
    urdfFilename = "package://gerard_bauzil/urdf/driller.urdf"
    srdfFilename = "package://gerard_bauzil/srdf/driller.srdf"
    rootJointType = "freeflyer"

class AircraftSkin:
    urdfFilename = "package://agimus_demos/urdf/aircraft_skin_with_marker.urdf"
    srdfFilename = "package://agimus_demos/srdf/aircraft_skin_with_marker.srdf"
    rootJointType = "anchor"

robot = Robot("tiago", rootJointType="planar")
robot.setJointBounds('root_joint', [-2, 2, -2, 2])
#robot.insertRobotSRDFModel("tiago", "tiago_data", "schunk", "_gripper")
ps = ProblemSolver(robot)
vf = ViewerFactory(ps)
#vf.loadRobotModel (Driller, "driller")
#robot.insertRobotSRDFModel("driller", "gerard_bauzil", "qr_drill", "")
#robot.setJointBounds('driller/root_joint', [-2, 2, -2, 2, 0, 2])
vf.loadObstacleModel(Driller.urdfFilename, "driller")
driller_pose = [-0.3, 1., 0.85, 0., 0., 0., 1.]
vf.moveObstacle('driller/base_link_0', driller_pose)
vf.loadObstacleModel('package://iai_maps/urdf/table.urdf', 'table')

ps.selectPathValidation("Dichotomy", 0)
ps.selectPathProjector("Progressive", 0.2)

##from hpp import Quaternion
##oMsk = (0.10576, -0.0168, 1.6835) + Quaternion().fromRPY(1.8, 0, 0).toTuple()
##oMsk = (0.30576, -0.0138, 1.5835) + Quaternion().fromRPY(1.8, 0, 0).toTuple()
##vf.loadObstacleModel(skinTagUrdf, "skin")
##vf.moveObstacle("skin", oMsk)
#vf.loadObjectModel (AircraftSkin, "skin")
##vf.loadRobotModelFromString ("skin", AircraftSkin.rootJointType, AircraftSkin.urdfString, AircraftSkin.srdfString)
##robot.setRootJointPosition("skin", oMsk)
##robot.setJointPosition("skin/root_joint", oMsk)

q0 = robot.getCurrentConfig()
q0[:4] = [1., 0.8, 0, 1]
q0[robot.rankInConfiguration['torso_lift_joint']] = 0.15
q0[robot.rankInConfiguration['arm_1_joint']] = 0.10
q0[robot.rankInConfiguration['arm_2_joint']] = -1.47
q0[robot.rankInConfiguration['arm_3_joint']] = -0.16
q0[robot.rankInConfiguration['arm_4_joint']] = 1.87
q0[robot.rankInConfiguration['arm_5_joint']] = -1.57
q0[robot.rankInConfiguration['arm_6_joint']] = 0.01
q0[robot.rankInConfiguration['arm_7_joint']] = 0.00

q0[robot.rankInConfiguration['hand_thumb_abd_joint']] = 1.5707

q0[robot.rankInConfiguration['hand_index_abd_joint']]  = 0.35
q0[robot.rankInConfiguration['hand_middle_abd_joint']] = -0.1
q0[robot.rankInConfiguration['hand_ring_abd_joint']]   = -0.2
q0[robot.rankInConfiguration['hand_little_abd_joint']] = -0.35

def lockJoint(jname, q, cname=None):
    if cname is None:
        cname = jname
    s = robot.rankInConfiguration[jname]
    e = s+robot.getJointConfigSize(jname)
    ps.createLockedJoint(cname, jname, q[s:e])
    ps.setConstantRightHandSide(cname, True)
    return cname

ljs = list()
#ljs.append(lockJoint("root_joint", q0))

for n in robot.jointNames:
    if n.startswith('hand_'):
        ljs.append(lockJoint(n, q0))

ps.createPositionConstraint("gaze", "xtion_rgb_optical_frame", "",
        (0,0,0), driller_pose[:3], (True,True,False))

end_eff_pos = driller_pose[:3] + [0,0,0,1]
end_eff_pos[0] -= 0.03
end_eff_pos[1] -= 0.03

ps.createTransformationConstraint("IK", "", "hand_grasping_fixed_joint", end_eff_pos, (True,)*6)

ps.addNumericalConstraints("test", ["IK"] + ljs)
success, q, err = ps.applyConstraints(robot.shootRandomConfig())
print(success, err)

v = vf.createViewer()
v(q)

import sys
sys.exit(0)
