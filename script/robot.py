from hpp.corbaserver.robot import Robot as Parent

class Robot (Parent):
    urdfFilename = "package://example-robot-data/robots/ur_description/urdf/ur5_joint_limited_robot.urdf"
    srdfFilename = "package://example-robot-data/robots/ur_description/srdf/ur5_joint_limited_robot.srdf"

    def __init__ (self, robotName, load = True, rootJointType = "anchor"):
        Parent.__init__ (self, robotName, rootJointType, load)
        self.rightWrist = "wrist_3_joint"
        self.leftWrist  = "wrist_3_joint"
        self.endEffector = "ee_fixed_joint"

    def getInitialConfig (self):
        q = 6*[0]
        return q
