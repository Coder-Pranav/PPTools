import advanced_Merge

toolbar = nuke.menu('Nodes')
c = toolbar.addMenu('PP Tools', 'pptool.png')
c.addCommand("Advanced Merge Tool",lambda: advanced_Merge.advanced_Merge(),"m",icon='pptool.png')