from hpp import Transform
from hpp.corbaserver.manipulation.robot import Robot
from hpp.corbaserver.manipulation import ProblemSolver
from hpp.gepetto.manipulation import ViewerFactory

class Pokeball (Robot):
  rootJointType = 'freeflyer'
  packageName = 'hpp_environments'
  meshPackageName = 'hpp_environments'
  urdfName = 'ur_benchmark/pokeball'
  urdfSuffix = ""
  srdfSuffix = ""

  def __init__ (self, name) :
    Robot.__init__ (self, "pokeballs", name, self.rootJointType)

robot = Pokeball ("pk1")
ps = ProblemSolver (robot)

vf = ViewerFactory (ps)
vf.loadObjectModel (Pokeball, 'pk2')

robot.setJointBounds ('pk1/root_joint', [-.4,.4,-.4,.4,-.1,1.,1,0,1,0,1,0,1,0])
robot.setJointBounds ('pk2/root_joint', [-.4,.4,-.4,.4,-.1,1.,1,0,1,0,1,0,1,0])

q1 = [.3, 0, 0.025, 0, 0, 0, 1, .3, 0, 0.025, 0, 0, 0, 1]

ps.createTransformationConstraint ('f1', 'pk1/root_joint', 'pk2/root_joint', [0,0,0.025,0,0,0,1], [False, False, True, True, True, False,])
ps.createTransformationConstraint ('f2', 'pk1/root_joint', 'pk2/root_joint', [0,0,0.025,0,0,0,1], [True, True, False, False, False, True,])
ps.createTransformationConstraint ('f3', 'pk1/root_joint', 'pk2/root_joint', [0,0,0.025,0,0,0,1], [True, True, True, True, True, True,])

ps.setNumericalConstraints("test", ["f1"])
