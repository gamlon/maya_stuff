import os
import shutil
import timeit
import time
import subprocess
import platform

from maya import cmds

FILE_NAME = 'xxx_air_c17-lidar_mdl_v003_kpm.ma'
TEST_NAME = 'xxx_air_c17-lidar_mdl_v003_kpm_test.ma'
LOCAL_PATH = r'C:\pxm_localfiles\temp'
NETWORK_PATH = r'X:\_pxm\filedata\app_trash\20160629\maya_test'


def save(path):
    cmds.file(rename=path)
    cmds.file(save=True, type='mayaAscii')
    return path


def alembic(path):
    cmds.refresh(suspend=True)
    path = path + ".abc"
    pm.AbcExport(j="-step 1 -fr 10 20 -worldSpace -uvWrite -renderableOnly -selection -f " + path)
    cmds.refresh(suspend=False)
    return path


def obj(path):
    path = cmds.file(path, typ="OBJexport", es=1, op="groups=0; ptgroups=0;materials=0; smoothing=1; normals=1")
    path = path.replace('/', '\\')
    return path


def fbx(path):
    mel.eval(('FBXExport -f \"{}\" -s').format(path.replace(os.sep, '/')))
    path += '.fbx'
    return path


def save_locally(func):
    path = os.path.join(LOCAL_PATH, TEST_NAME)
    func(path)


def save_network1(func):
    path = os.path.join(NETWORK_PATH, TEST_NAME)
    func(path)


def save_network3(func):
    path_local = os.path.join(LOCAL_PATH, TEST_NAME)
    path_net = os.path.join(NETWORK_PATH, TEST_NAME)
    path = func(path_local)
    copy_path = NETWORK_PATH+'\\'+path.split('\\')[-1]
    size_of_file = get_file_size(path)
    start_copy = time.time()

    if platform.system() == 'Windows':
        proc = subprocess.Popen('xcopy "%s" "%s" /Y ' % (path, NETWORK_PATH))
        proc.wait()
    else:
        shutil.copy(path, copy_path)
    print 'Copied with %.2f  MB/s' % (size_of_file/(time.time() - start_copy))


def get_file_size(path_):
    try:
        return os.path.getsize(path_)/1024.0/1024.0
    except WindowsError:
        return 0


print(timeit.timeit("save_locally(save)", setup="from __main__ import save_locally, save", number=1))
print(timeit.timeit("save_network1(save)", setup="from __main__ import save_network1, save", number=1))
print(timeit.timeit("save_network3(save)", setup="from __main__ import save_network3, save", number=1))