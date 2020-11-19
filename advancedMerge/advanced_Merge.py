# --------------------------------------------------------------
#  advanced_Merge2.py
#  Version: 3.0.0
#  Last Updated: August 1, 2019
#  Written by Pranav Pradeep
#  Thank You  Mads Hagbarth & Satheesh Rengasamy for helping out
#  For detailed instructions: https://boovovfx.wordpress.com/
# --------------------------------------------------------------

# --------------------------------------------------------------
#  USAGE:
#  Type the name of the operation in the input box and it will create the merge with that operation
#  Few shortcuts for major operations:
#  Mask = 'm'
#  Over = 'o'
#  Stencil = 's'
#  Minus = '-'
#  Plus = '+'
#  Multiply = '*'
#  Matte = 'a'
#  Under = 'u'
#  From = 'f'
#  Min = '--'
#  Max = '++'
#  Difference = 'd'
#  Divide = '/'
#  Screen = 'r'
# --------------------------------------------------------------
# Add this to menu.py

# import advanced_Merge2

# toolbar=nuke.menu('Nodes')
# me=toolbar.addMenu('Advanced Merge','Merge.png')
# me.addCommand("Advanced Merge Tool",lambda: advanced_Merge2.advanced_Merge2(),"m")
# --------------------------------------------------------------


try:
    from PySide.QtGui import *
    from PySide.QtCore import *
except ImportError:
    from PySide2.QtCore import *
    from PySide2.QtWidgets import *
import nuke

merge_operations = ['atop', 'average', 'color-burn', 'color-dodge', 'conjoint-over', 'copy', 'difference',
                    'disjoint-over', 'divide', 'exclusion', 'from', 'geometric', 'hard-light', 'hypot', 'in',
                    'mask', 'matte', 'max', 'min', 'minus', 'multiply', 'out', 'over', 'overlay', 'plus',
                    'screen', 'soft-light', 'stencil', 'under', 'xor']


class Panel(QWidget):
    def __init__(self):
        super(Panel, self).__init__()

        layout = QHBoxLayout()

        label = QLabel('Search Operation:')
        layout.addWidget(label)

        # QLine Edit
        self.line = QLineEdit()
        self.line.setPlaceholderText('Type Here')
        self.line.setStyleSheet("margin: 2.5px; padding: 2.5px; \
                                 background-color: \
                                 rgba(0, 0, 1,255);\
                                 color: rgba(130, 76, 113,255); \
                                 border-style: solid; \
                                 border-radius: 10px; \
                                 border-width: 1px; \
                                 border-color: \
                                 rgba(144, 170, 134,255);")
        layout.addWidget(self.line)

        # Qcompleter
        completer = QCompleter(merge_operations)
        self.line.setCompleter(completer)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.popup().setAlternatingRowColors(True)
        completer.popup().setStyleSheet("background-color: \
                                 rgba(50, 50, 50,255); \
                                 color: rgba(220, 204, 163,255);\
                                 alternate-background-color:\
                                 rgba(68, 68, 68,255);\
                                 border-style: solid; \
                                 border-radius: 8px; \
                                 border-width: 1px; \
                                 border-color: \
                                 rgba(144, 170, 134,255);")

        # QCheckBox
        self.checkbox = QCheckBox('Change Operation')
        self.checkbox.setToolTip('Helps you to change the operation of selected merges')
        self.checkbox.setStyleSheet("background-color: \
                           rgba(50, 50, 50,255); \
                           color: rgba(220, 204,163,255);")
        layout.addWidget(self.checkbox)


        # signals,layouts and stylesheet
        self.line.returnPressed.connect(self.user_input)
        self.checkbox.clicked.connect(self.chkbox_clicked)
        self.setStyleSheet("background-color: \
                           rgba(50, 50, 50,255); \
                           color: rgba(220, 204, 163,255); ")

        self.setLayout(layout)
        self.setWindowTitle('Advanced Merge Panel')
        # print layout.sizeHint()
        self.setMinimumSize(450, 52)
        self.setMaximumSize(450, 52)

    def chkbox_clicked(self):
        return self.checkbox.isChecked()

    # Actual Logic of the program starts here(for nuke)
    def user_input(self):
        self.text = self.line.text().lower()
        # print self.text
        self.close()

        my_shortcut = {'m': 'mask', 'o': 'over', 's': 'stencil', '+': 'plus', '-': 'minus',
                   '*': 'multiply', 'a': 'matte', 'u': 'under', 'f': 'from',
                   '--': 'min', '++': 'max', 'd': 'difference', '/': 'divide', 'r': 'screen'}

        usr_input = self.text
        for key in my_shortcut:
            if key == usr_input:
                usr_input = my_shortcut[key]
                break

            else:
                usr_input = usr_input

        if usr_input not in merge_operations:
            nuke.message('Bummer!, No Such Operation')
        else:
            if self.chkbox_clicked():
                selected_nodes = nuke.selectedNodes()
                if not selected_nodes:
                    nuke.message("Oops! You haven't selected anything")
                else:
                    found = False
                    for i in selected_nodes:
                        try:
                            if i['operation'].getValue() is not None:
                                found = True
                                i['operation'].setValue(merge_operations.index(usr_input))

                        except:
                            pass
                    if not found:
                        nuke.message("Hey! You selected the wrong node")
            else:
                K = nuke.createNode('Merge2')
                O = K.knob('operation').setValue(merge_operations.index(usr_input))


def advanced_Merge():
    advanced_Merge.panel = Panel()
    advanced_Merge.panel.setWindowFlags(
        Qt.Window |
        Qt.CustomizeWindowHint |
        Qt.WindowTitleHint |
        Qt.WindowCloseButtonHint |
        Qt.WindowStaysOnTopHint
        )
    advanced_Merge.panel.show()