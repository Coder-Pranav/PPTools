import nuke

import nukeSearcher

toolbar = nuke.menu('Nodes')
c = toolbar.addMenu('PP Tools', 'pptool.png')
c.addCommand('Nuke API Searcher', lambda: nukeSearcher.nukeSearcher(), '', icon='pptool.png')
