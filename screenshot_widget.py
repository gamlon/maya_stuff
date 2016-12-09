from PySide import QtGui

import pymel.core as pm

from data_access import file_handling
from exchange import tagging

def main():
    cams = tagging.ListTag(tagging.TAG_RENDER_CAMERA, True)

    if not cams:
        pm.warning("No or more then one tagged camera in scene file!")
        return

    name = '.camera_rotation_{0}'

    file_ = file_handling.mayaFile.fromFile(pm.sceneName())

    for cam in cams:
        cam_trans = cam.getParent()
        new_name = name.format(cam_trans.name())
        pub_file = file_.get_publish_file(new_name, '.jpg')
        pm.select(clear=1)
        pm.select(cam_trans.r)
        editor_name = 'Graph Editor'
        title_ = '%s %s' % (cam_trans.name(), editor_name)
        window_ = create_screenshot_layout('animCurveEditor', title_)

        maya.utils.executeDeferred(create_screenshot, window_, pub_file)


def create_screenshot_layout(editor_, title_):
    """Creates a pymel window with the editor passed as an argument.
    Args:
        editor_: string defining the pymel.windows function to call
        title_: title of the widget
    Returns:
        Pymel Window UI: The layout window to take a screenshot of
    """
    layout_window = pm.window(title_)
    pm.frameLayout(title_)
    pm.mel.eval(editor_ + '()')
    pm.showWindow()
    layout_window.asQtObject().showMaximized()
    pm.setFocus(layout_window)
    return layout_window


def create_screenshot(window_, pub_file):
    """creates a screenshot of the window_`s panel
    Args:
        window_: PyMel Window UI to take a snapshot of
        pub_file: the file incl. path to store the screenshot
    """
    print 'creating screenshot in %s' % pub_file
    originalPixmap = QtGui.QPixmap.grabWidget(window_.asQtObject())
    originalPixmap.save(pub_file)
    pm.deleteUI(window_)


main()

