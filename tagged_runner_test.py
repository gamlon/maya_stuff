"""
help('gen_file-handling')
# Create object named selection and type - SelectionList
selection = OpenMaya.MSelectionList()
# Fill variable "selection" with list of selected objects
OpenMaya.MGlobal.getActiveSelectionList(selection)
# Create iterator through list of selected object
selection_iter = OpenMaya.MItSelectionList(selection)
obj = OpenMaya.MObject()
dagNodeFn = OpenMaya.MFnDagNode()

numShapesUtil = OpenMaya.MScriptUtil()
numShapesUtil.createFromInt(0)
numShapesPtr = numShapesUtil.asUintPtr()
# Loop though iterator objects
while not selection_iter.isDone():
    # Now we can do anything with each of selected objects.
    # In this example lets just print path to iterating objects.
    selection_iter.getDependNode(obj)
    dag_path = OpenMaya.MDagPath.getAPathTo(obj)
    dagNodeFn.setObject(obj)
    dir(dagNodeFn.typeName().__name__)
    dir(type(dag_path)
    selection_iter.next()
"""
import time

from exchange import tagging

from maya import OpenMaya
import pymel.core as pm
from maya import cmds


def get_tagged2(attr):
    start_ = time.time()
    names = []
    dagIterator = OpenMaya.MItDag(OpenMaya.MItDag.kDepthFirst,
                                  OpenMaya.MFn.kInvalid)

    numShapesUtil = OpenMaya.MScriptUtil()
    numShapesUtil.createFromInt(0)
    numShapesPtr = numShapesUtil.asUintPtr()

    # This reference to the MFnDagNode function set will be needed
    # to obtain information about the DAG objects.
    dagNodeFn = OpenMaya.MFnDagNode()

    while not dagIterator.isDone():
        dag_object = dagIterator.currentItem()

        dagNodeFn.setObject(dag_object)

        dag_path = OpenMaya.MDagPath.getAPathTo(dag_object)
        try:
            dag_path.numberOfShapesDirectlyBelow(numShapesPtr)
        except:
            dagIterator.next()

        if dagNodeFn.hasAttribute(attr) and dagNodeFn.findPlug(attr,
                                                               True).asBool():
            if OpenMaya.MScriptUtil(numShapesPtr).asUint():
                names.append(pm.PyNode(dagNodeFn.name()))

        dagIterator.next()

    print time.time() - start_
    return names


def get_tagged(attr):
    start_ = time.time()
    numShapesUtil = OpenMaya.MScriptUtil()
    numShapesUtil.createFromInt(0)
    numShapesPtr = numShapesUtil.asUintPtr()

    names = []

    transform_iter = OpenMaya.MItDependencyNodes(OpenMaya.MFn.kTransform)
    dagNodeFn = OpenMaya.MFnDagNode()

    while not transform_iter.isDone():
        transform_mObject = transform_iter.thisNode()

        dag_path = OpenMaya.MDagPath.getAPathTo(transform_mObject)
        dag_path.numberOfShapesDirectlyBelow(numShapesPtr)

        dagNodeFn.setObject(dag_path)
        if dagNodeFn.hasAttribute(attr) and dagNodeFn.findPlug(attr,
                                                               True).asBool():
            if OpenMaya.MScriptUtil(numShapesPtr).asUint():
                names.append(pm.PyNode(dag_path))

        transform_iter.next()

    print time.time() - start_
    return names


def get_tagged_tagging():
    start_time = time.time()
    geo_list = tagging.ListTag(tagging.TAG_EXPORT_GEOMETRY, True)
    print time.time() - start_time
    return geo_list


def get_tagged_cmds(attr):
    start_time = time.time()
    names = []
    for obj in cmds.ls(type='mesh'):
        try:
            parent_ = cmds.listRelatives(obj, parent=True)[0]
            if cmds.getAttr(parent_ + '.' + attr):
                names.append(pm.PyNode(parent_))
        except ValueError:
            pass
    print time.time() - start_time
    return names


def get_tagged_cmds_transforms(attr):
    start_time = time.time()
    names = []
    for obj in cmds.ls(type='transform'):
        try:
            if cmds.listRelatives(obj, children=True, shapes=True)[0]:
                if cmds.getAttr(obj + '.' + attr):
                    names.append(pm.PyNode(obj))
        except (TypeError, ValueError):
            pass
    print time.time() - start_time
    return names


attr = '_'.join(
    tagging.TagSetting.get(tagging.TAG_EXPORT_GEOMETRY, True)['name'])
names = get_tagged(attr)
names2 = get_tagged2(attr)
names_tagged = get_tagged_tagging()
names_cmds = get_tagged_cmds(attr)
names_cmds_transform = get_tagged_cmds_transforms(attr)

print len(names)
print len(names2)
print len(names_cmds)
print len(names_cmds_transform)
print len(names_tagged)
