import json
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtCore import *
import sys
import textwrap
import webbrowser
import os

# --------------------------------------------------------------
#  Nuke API Searcher
#  Version: 1.0.0
#  Last Updated: June 24, 2020
#  Written by Pranav Pradeep
# --------------------------------------------------------------

# --------------------------------------------------------------
# How to install
# --------------------------------------------------------------
# Unzip NukeSearcher.zip and put "NukeSearcher" folder in .nuke folder
# Add this to init.py in .nuke folder
# nuke.pluginAddPath('./NukeSearcher')
# Open Nuke
# --------------------------------------------------------------


path = os.path.dirname(os.path.realpath(__file__))+'/json/'

"""importing different json files with information"""


with open(path +'nk_api.json', 'r') as openfile:
    json_read = json.load(openfile)

with open(path +'nk_api_info.json', 'r') as openfile_info:
    json_read_info = json.load(openfile_info)

with open(path + 'nk_api_links_V002.json', 'r') as openfile_links:
    json_read_link = json.load(openfile_links)



def nuke_info(word):
    """this function gives the text information based on search result"""

    for i in json_read_info:
        try:
            return textwrap.dedent(i[word])  # textwrap is optional
        except:
            pass


def nuke_link(word):
    """this function gives the link information based on search result"""

    for i in json_read_link:
        try:
            return i[word].encode('utf-8')
        except:
            pass


class Panel(QWidget):
    """pyside2 starts here and all panel and ui"""

    def __init__(self):
        super(Panel, self).__init__()

        self.layout = QVBoxLayout()

        self.font = QFont()
        self.font.setPointSize(15)

        """setting buttons"""

        self.button1 = QPushButton('Open in browser')
        self.button1.setMinimumHeight(50)
        self.button1.setStyleSheet("background-color: rgba(238, 162, 67,255);")
        self.button1.setFont(self.font)


        """setting checkbox for filtering"""

        self.checkBox = QCheckBox('filter_startswith')
        self.checkBox.setStyleSheet('color: rgba(238, 162, 67,255);')


        """setting auto complete for line edit """

        self.completer = QCompleter(json_read)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer.setFilterMode(Qt.MatchContains)
        self.completer.setMaxVisibleItems(20)
        self.completer.popup().setFont(self.font)
        self.completer.popup().setAlternatingRowColors(True)
        self.completer.popup().setStyleSheet("color: rgba(238, 162, 67,255);")

        """ setting line edit """
        self.lineEdit = QLineEdit()
        self.lineEdit.setCompleter(self.completer)
        self.lineEdit.setTextMargins(50, 50, 50, 50)


        """font settings for line edit"""
        f = self.lineEdit.font()
        f.setBold(True)
        f.setPointSize(27)
        self.lineEdit.setFont(f)
        self.lineEdit.setStyleSheet("margin: 2.5px; padding: 2.5px; \
                                 color: rgba(238, 162, 67,255); \
                                 border-style: solid; \
                                 border-radius: 10px; \
                                 border-width: 1px;")


        """settings for Text Edit"""

        self.textEdit = QTextEdit()
        self.textEdit.setStyleSheet("margin: 2.5px; padding: 2.5px; \
                                                color: rgba(238, 162, 67,255); \
                                                border-style: solid; \
                                                border-radius: 10px; \
                                                border-width: 1px;")
        self.textEdit.setWordWrapMode(QTextOption.WordWrap)


        """setting font settings for Text edit"""

        tx_font = self.lineEdit.font()
        tx_font.setFamily('Helvetica')
        tx_font.setBold(False)
        tx_font.setPointSize(15)
        self.textEdit.setFont(tx_font)


        """All layout settings """
        self.layout.addWidget(self.checkBox)
        self.layout.addWidget(self.lineEdit)
        self.setLayout(self.layout)
        self.setMinimumWidth(800)
        self.setMinimumHeight(200)
        self.setWindowTitle('Nuke API Searcher')

        """all signals"""

        self.lineEdit.returnPressed.connect(self.lala)
        self.checkBox.stateChanged.connect(self.comb_box_click)
        self.button1.clicked.connect(self.button1_press)

    #        self.setStyleSheet("background-color: rgba(73, 73, 73,255);")

    def lala(self):
        """This function is executed when Enter is pressed in line edit"""

        var = str(self.lineEdit.text())
        self.layout.addWidget(self.textEdit)
        self.layout.addWidget(self.button1)

        self.textEdit.document().setPlainText(nuke_info(var))

        font = self.textEdit.document().defaultFont()
        fontMetrics = QFontMetrics(font)
        textSize = fontMetrics.size(0, self.textEdit.toPlainText())

        w = textSize.width() + 10
        h = textSize.height() + 10
        self.resize(800, h * 3)
        if self.height() <= 350:
            self.resize(800, 350)
        else:
            pass
        self.textEdit.setReadOnly(True)
        self.setMinimumHeight(350)
        self.setMaximumHeight(700)

    def comb_box_click(self):
        """executes on checkbox ticked/clicked.Use to filter search results starting with words typed """

        if self.checkBox.isChecked():
            self.completer.setFilterMode(Qt.MatchStartsWith)
        else:
            self.completer.setFilterMode(Qt.MatchContains)

    def button1_press(self):
        """open link in browser fore corresponding search term"""

        ext = nuke_link(str(self.lineEdit.text()))
        url = 'https://learn.foundry.com/nuke/developers/70/pythonreference/{}'.format(ext)
        webbrowser.open(url)


def nukeSearcher():
    nukeSearcher.panel = Panel()
    nukeSearcher.panel.show()





