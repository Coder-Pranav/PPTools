import nuke
from pathFIles import *

menu = nuke.menu('Nuke')
gizmo_menu = menu.addMenu('Gizmos')
basepath = GIZMOS_PATH
dir_files = os.listdir(basepath)
icon_folder = ICONS_PATH


def addToMenu(p_gizmo):
    giz_name = p_gizmo.split('.')[0]
    if os.path.isfile(icon_folder+'/'+giz_name+'.png'):
        gizmo_menu.addCommand(giz_name, 'nuke.createNode("{}")'.format(giz_name))
    else:
        gizmo_menu.addCommand(giz_name, 'nuke.createNode("{}")'.format(giz_name), icon='pptool.png')

for file in dir_files:
    if file.endswith('.gizmo'):
        addToMenu(file)

