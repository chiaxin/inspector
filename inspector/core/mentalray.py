#
#
#
import maya.cmds as mc

gMiaShaders = ('mia_material_x', 'mia_material_x_passes')

def pblm_isBumpNormalError():
    '''Mental Ray Bump Normal Error'''
    global gMiaShaders
    if not mc.pluginInfo('Mayatomr', q=True, l=True):
        print '// Mental Ray Plug-in is not loaded, ignore.'
        return []
    check_attribues = ('standard_bump', 'overall_bumpX',
        'standard_bumpX', 'standard_bumpY', 'standard_bumpZ',
        'overall_bumpX', 'overall_bumpY', 'overall_bumpZ')
    def _isError(shader):
        if not mc.connectionInfo(shader+'.standard_bump', id=True):
            for a in ('.standard_bumpX', '.standard_bumpY', '.standard_bumpZ'):
                if mc.getAttr(shader+a) != 0:
                    return False
        if not mc.connectionInfo(shader+'.overall_bump', id=True):
            for a in ('.overall_bumpX', '.overall_bumpY', '.overall_bumpZ'):
                if mc.getAttr(shader+a) != 0:
                    return False
        return True
    return [sd for sd in mc.ls(type=gMiaShaders) if not _isError(sd)]

def solve_isBumpNormalError(err_items):
    '''Mental Ray Bump Normal Error'''
    if not mc.pluginInfo('Mayatomr', q=True, l=True):
        print '// Mental Ray Plug-in is not loaded, ignore.'
        return []
    fix_list = []
    for item in items:
        if not mc.connectionInfo(item+'.standard_bump'):
            mc.setAttr(item+'.standard_bumpX', 0)
            mc.setAttr(item+'.standard_bumpY', 0)
            mc.setAttr(item+'.standard_bumpZ', 0)
            fix_list.append(item)
        if not mc.connectionInfo(item+'.overall_bump'):
            mc.setAttr(item+'.overall_bumpX', 0)
            mc.setAttr(item+'.overall_bumpY', 0)
            mc.setAttr(item+'.overall_bumpZ', 0)
            fix_list.append(item)
    # Remove duplicated item
    return tuple(set(fix_list))
