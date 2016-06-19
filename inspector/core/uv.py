#
#
#

import maya.cmds as mc

gUvOutOfRangeMin = (-1.0, 1.0)
gUvOutOfRangeMax = ( 1.0, 1.0)

def pblm_multiUVsetMesh():
    '''Multi UV Set'''
    multiUVset_ret = []
    for mesh in mc.ls(type='mesh', l=True):
        allUVsets = mc.polyUVSet(mesh, q=True, auv=True)
        if len(allUVsets) > 1:
            multiUVset_ret.append(mesh)
    return multiUVset_ret

def solve_multiUVsetMesh(err_items):
    '''Multi UV Set'''
    return []

def pblm_uvSetNotMap1Mesh():
    '''UV Set is Not Map1'''
    uvSetNotMap1_ret = []
    for mesh in mc.ls(type='mesh', l=True):
        currUVset = mc.polyUVSet(mesh, q=True, cuv=True)
        if currUVset[0] != 'map1':
            uvSetNotMap1_ret.append(mesh)
    return uvSetNotMap1_ret

def solve_uvSetNotMap1Mesh(err_items):
    '''UV Set is Not Map1'''
    return []

def pblm_uvOutOfRange():
    '''UV Out of Range'''
    global gUvOutOfRangeMin
    global gUvOutOfRangeMax
    out_of_range_meshes = []
    for mesh in mc.ls(type='mesh', l=True):
        numOfUV = mc.polyEvaluate(mesh, uv=True)
        for idx in range(numOfUV):
            uvpos = mc.polyEditUV(mesh+'.map['+str(idx)+']', q=True)
            if uvpos[0] <= gUvOutOfRangeMin[0] \
                or uvpos[0] >= gUvOutOfRangeMin[1] \
                or uvpos[1] <= gUvOutOfRangeMax[0] \
                or uvpos[1] >= gUvOutOfRangeMin[1]:
                # out of range uv point
                out_of_range_meshes.append(mesh)
    return tuple(set(out_of_range_meshes))

def solve_uvOutOfRange(err_items):
    '''UV Out of Range'''
    return []
