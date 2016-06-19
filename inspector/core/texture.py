#
# Module : texture
#
import maya.cmds as mc

'''
    Configure Define
'''
gAlphaIsLuminanceKeywords = ('Bmp', 'Nml', 'rlAmo', 'rrAmo', 'Gls')
# off:0, midmap:1, box:2, quadratic:3, quartic:4, gaussian:5
gTextureFilterType = 1
# defaultColor, colorGain, colorOffset, alphaGain, alphaOffset
gColorBalanceCheckAttributes = (0, 1, 1, 1, 1)
gColorBalanceAttribures = (
    ('defaultColorR', 'defaultColorG', 'defaultColorB'),
    ('colorGainR', 'colorGainG', 'colorGainB'),
    ('colorOffsetR', 'colorOffsetG', 'colorOffsetB'),
    'alphaGain', 'alphaOffset')
gColorBalanceDefAttribures = (
    (0.5, 0.5, 0.5), (1.0, 1.0, 1.0), (0.0, 0.0, 0.0), 1.0, 0.0)
# Effect Filter
gEffectFilter = 1.0

def pblm_alphaIsLuminanceIsNotOn():
    '''Alpha is Luminance is not ON'''
    global gAlphaIsLuminanceKeywords
    textures = mc.ls(type='file')
    error_ret = [tex for tex in textures for kw in gAlphaIsLuminanceKeywords
        if tex.find(kw) >= 0 and not mc.getAttr(tex+'.alphaIsLuminance')]
    return error_ret

def solve_alphaIsLuminanceIsNotOn(err_items):
    '''Alpha is Luminance is not ON'''
    fix_list = []
    for item in err_items:
        if mc.getAttr(item+'.alphaIsLuminance') != 1:
            mc.setAttr(item+'alphaIsLuminance', 1)
            fix_list.append(item)
    return fix_list

def pblm_textureFilterTypeIncorrect():
    '''Texture Filter Type Incorrect'''
    global gTextureFilterType
    return [tex for tex in mc.ls(type='file')
        if mc.getAttr(tex+'.filterType') != gTextureFilterType]

def solve_textuteFilterTypeIncorrect(err_items):
    '''Texture Filter Type Incorrect'''
    global gTextureFilterType
    fix_list = []
    for item in err_items:
        if mc.getAttr(item+'.filterType') != gTextureFilterType:
            mc.setAttr(item+'.filterType', gTextureFilterType)
            fix_list.append(item)
    return fix_list

def pblm_textureColorBalanceIncorrect():
    '''Texture Color Balance Incorrect'''
    global gColorBalanceCheckAttributes
    global gColorBalanceAttribures
    global gColorBalanceDefAttribures
    def _check(item):
        for idx, attr in enumerate(gColorBalanceAttribures):
            if gColorBalanceCheckAttributes[idx] != 1:
                continue
            if isinstance(attr, tuple):
                for eidx, elem in enumerate(attr):
                    if mc.getAttr(item+'.'+elem) != gColorBalanceDefAttribures[idx][eidx]:
                        return False
            else:
                if mc.getAttr(item+'.'+attr) != gColorBalanceDefAttribures[idx]:
                    return False
        return True
    return [tex for tex in mc.ls(type='file') if not _check(tex)]

def solve_textuteColorBalanceIncorrect(err_items):
    '''Texture Color Balance Incorrect'''
    return []

def pblm_textureFilterValueIncorrect():
    '''Texture Filter Value Incorrect'''
    global gEffectFilter
    return [tex for tex in mc.ls(type='file') 
        if mc.getAttr(tex+'.filter') != gEffectFilter]

def solve_textureFilterValueIncorrect(err_items):
    '''Texture Filter Value Incorrect'''
    global gEffectFilter
    fix_list = []
    for item in err_items:
        if mc.getAttr(item+'.filter') != gEffectFilter:
            mc.setAttr(item+'.filter', gEffectFilter)
            fix_list.append(item)
    return fix_list

def pblm_fileTextureNameIsEmpty():
    '''Texture File Texture Name is Empty'''
    return [tex for tex in mc.ls(type='file')
        if not mc.getAttr(tex+'.fileTextureName')]

def solve_fileTextureNameIsEmpty(err_items):
    '''Texture File Texture Name is Empty'''
    return []
