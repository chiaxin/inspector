#################################################
# Author : Chia Xin Lin
# Version : 0.0.1
# Last Update : Jun 18, 2016
#################################################
import argparse
import sys
import types
import os
import os.path
import core
import maya.standalone
import maya.cmds as mc
maya.standalone.initialize()

VERSION = '0.0.1'
REPORT_CSV_SUFFIX = '_report.csv'
AUTOFIX_FILE_SUFFIX_MA = '_solve.ma'
AUTOFIX_FILE_SUFFIX_MB = '_solve.mb'

# Auto capture the module and function in module-core
# classifies pblm & solve function separately.
# pblm_ -> inspect problems, solve_ -> solutions
# import all member module in core
__import__('core', globals(), locals(), core.__all__, 0)
pblm_functions = list()
solve_functions = list()
pblm_issue_maps = dict()
solve_issue_maps = dict()
collect_modules = [core.__dict__.get(m) for m in dir(core)
    if isinstance(core.__dict__.get(m), types.ModuleType)]
for module in collect_modules:
    functions = [module.__dict__.get(a) for a in dir(module)
        if isinstance(module.__dict__.get(a), types.FunctionType)]
    for func in functions:
        if func.__name__.find('pblm') == 0:
            pblm_functions.append(func)
        elif func.__name__.find('solve') == 0:
            solve_functions.append(func)
for func in pblm_functions:
    pblm_issue_maps[func.__doc__] = func
for func in solve_functions:
    solve_issue_maps[func.__doc__] = func
# Delete temp functions list
del pblm_functions
del solve_functions

def _record(function, log, title):
    try:
        err_items = function()
        if err_items:
            log.write(title+',')
            map(lambda item: log.write(item+','), err_items)
            log.write('\n\r')
    except:
        sys.stderr.write('Failed in inspect : '+function.__name__)
        raise
    return err_items

def _solve(function, err_items, log, title):
    try:
        if not function:
            return []
        fix_items = function(err_items)
        if not fix_items:
            return []
        log.write(title+'[AUTOFIX],')
        map(lambda item: log.write(item+','), fix_items)
        log.write('\n\r')
        return []
    except:
        sys.stderr.write('Failed in solution : '+function.__name__)
        raise

def _parse_arg(command_line):
    # This help function can throw error when file is not find.
    def _file_is_exists(data_):
        if not os.path.isfile(data_):
            msg = '{0} is not exists!'.format(data_)
            raise argparse.ArgumentTypeError(msg)
        return data_
    # ArgumentParser Init
    parse = argparse.ArgumentParser(
        description='Inspector : Maya Check & Auto-Fix Package. ver '+VERSION)
    # Add argument flag
    parse.add_argument('-s', '--solve',
        action='store_true', help='Go auto fix after check.')
    parse.add_argument('data', type=_file_is_exists,
        help='The Maya files specific(ma or mb)')
    return parse.parse_args(command_line)

def _save_as_mayafile():
    global AUTOFIX_FILE_SUFFIX_MA
    global AUTOFIX_FILE_SUFFIX_MB
    save_file = ''
    maya_format = 'mayaAscii'
    currect_file = mc.file(q=True, sn=True).replace('\\', '/')
    if currect_file[-3:] == '.ma':
        save_file = currect_file[:-3] + AUTOFIX_FILE_SUFFIX_MA
    elif currect_file[-3:] == '.mb':
        save_file = currect_file[:-3] + AUTOFIX_FILE_SUFFIX_MB
        maya_format = 'mayaBinary'
    else:
        save_file = org_file + suffix
    mc.file(rename=save_file)
    mc.file(save=True, force=True, type=maya_format, uiConfiguration=False)
    return save_file

def main():
    global pblm_issue_maps
    global solve_issue_maps
    try:
        # Get parse data from argument line
        parse = _parse_arg(sys.argv[1:])
        # Argument flag collect
        maya_file_set = parse.data
        with_auto_fix = parse.solve
        # If data is single, let it into list
        if not isinstance(maya_file_set, list):
            maya_file_set = [maya_file_set.replace('\\', '/')]
        else:
            maya_file_set = map(lambda s: s.replace('\\', '/'), maya_file_set)
    except:
        sys.stderr.write('Failed to parse argument.')
        raise
    # Loop in specific maya files
    for maya_file in maya_file_set:
        if not os.path.isfile(maya_file):
            print '{0} is not exists!'.format(maya_file)
            continue
        try:
            without_ext_path = os.path.splitext(maya_file)
            doc = without_ext_path[0].replace('\\', '/') + REPORT_CSV_SUFFIX
            log = open(doc, 'w')
        except:
            print '{0} can\'t open, please check it is not occupied now.'
            raise
        try:
            mc.file(maya_file, force=True, open=True)
            for key in pblm_issue_maps.keys():
                err_items = _record(pblm_issue_maps[key], log, key)
                if with_auto_fix and err_items:
                    _solve(solve_issue_maps.get(key, None), 
                        err_items, log, key)
        except:
            sys.stderr.write('Failed in solve process')
            raise
        finally:
            log.close()
        if with_auto_fix:
            print 'Solved File Saved : ', _save_as_mayafile()

if __name__=='__main__':
    main()
