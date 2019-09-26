import PythonQt

main = PythonQt.gepetto.MainWindow.instance()
osg = main.osg()

hppfcl = main.getFromSlot ("addBV")
assert hppfcl is not None

meshfile = "/home/jmirabel/devel/demo/install/share/ur_description/meshes/ur5/collision/forearm.stl"
osg.createWindow ("t")
osg.addMesh ("mesh", meshfile)
hppfcl.addBV ("bvhmodel_0", meshfile, 0)
hppfcl.addBV ("bvhmodel_1", meshfile, 1)
hppfcl.addBV ("bvhmodel_2", meshfile, 2)
osg.addToGroup ("mesh", "t")
osg.addToGroup ("bvhmodel_0", "t")
osg.addToGroup ("bvhmodel_1", "t")
osg.addToGroup ("bvhmodel_2", "t")
osg.setVisibility ("bvhmodel_0", "OFF")
osg.setVisibility ("bvhmodel_2", "OFF")
