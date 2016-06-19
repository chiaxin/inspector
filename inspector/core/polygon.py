#
#
#
import maya.cmds as mc

gRenderStatsAttrs = ('castsShadows', 'receiveShadows',
        'motionBlur', 'primaryVisibility', 'smoothShading',
        'visibleInReflections', 'visibleInRefractions',
        'doubleSided', 'opposite')
gRenderStatsValues = (1, 1, 1, 1, 1, 1, 1, 1, 0)

def pblm_renderStatsIncorrect():
    '''Polygon Render Stats is not Correct'''
    global gRenderStatsAttrs
    global gRenderStatsValues
    def _check(mesh):
        check_list = tuple([mc.getAttr(mesh+'.'+a) for a in gRenderStatsAttrs])
        return check_list == gRenderStatsValues
    all_poly_without_im = mc.ls(type='mesh', l=True, ni=True)
    return [poly for poly in all_poly_without_im if not _check(poly)]

def solve_renderStatsIsNotCorrect(err_items):
    '''Polygon Render Stats is not Correct'''
    global gRenderStatsAttrs
    global gRenderStatsValues
    fix_list = []
    for poly in err_items:
        for idx, attr in enumerate(gRenderStatsAttrs):
            if mc.getAttr(poly+'.'+attr) != gRenderStatsValues[idx]:
                mc.setAttr(poly+'.'+attr, gRenderStatsValues[idx])
                fix_list.append(poly)
    return tuple(set(fix_list))
