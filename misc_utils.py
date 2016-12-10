import random

import pymel.core as pm


def create_variance_shader(shaders, varieties=5):
    """Creates n-varieties of colors for the passed shaders.
    Args:
        shaders (PyNode): Shader
        varieties (int): number of varieties to create
    """
    for shd in shaders:
        sg = shd.shadingGroups()[0]
        if sg and sg.type() == "shadingEngine":
            switch_ = pm.shadingNode("tripleShadingSwitch", asUtility=1)
            colorConst = []
            # setup color
            for i in range(varieties):
                colorConst.append(pm.shadingNode("ramp", asUtility=1))
                colorConst[i].colorEntryList[1].remove()
                colorConst[i].colorEntryList[0].color.set(random.random(),
                                                          random.random(),
                                                          random.random())

            # setup geo and connect random color
            for i, geo in enumerate(sg.members()):
                if not geo.name() == "shaderBallGeomShape1":
                    geo.instObjGroups[0] >> switch_.input[i].inShape
                    colorConst[random.randrange(0, varieties)].outColor >> \
                    switch_.input[i].inTriple

            switch_.output >> shd.color