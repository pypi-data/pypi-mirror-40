#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import json
import subprocess
from json2html import *

# 2 next lines: quit on Ctrl-C in terminal (stackoverflow.com/questions/4938723)
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

from src import conll

from PyQt5.QtWidgets import (
    qApp, QWidget, QPushButton, QSlider, QSplitter, QAbstractItemView,
    QLabel, QHBoxLayout, QVBoxLayout, QApplication, QScrollArea,
    QTreeView, QAction, QMainWindow, QFileDialog,QMessageBox
)

from PyQt5 import QtWebEngineWidgets

from PyQt5.QtCore import QUrl, Qt, QFileSystemWatcher, pyqtSignal, QObject
from PyQt5.QtGui import *


# create a new signal [redraw] for connection of arrow navigation in the treeview
class Communicate(QObject):
    redraw = pyqtSignal()

# a new TreeView widget is needed for redefinition of [currentChanged]
class MyTreeView(QTreeView):
    current_index = None
    def currentChanged(self,x,y):
        self.current_index = x
        self.c.redraw.emit()

class Dep2pict(QMainWindow):
    def __init__(self, screen, parent = None):
        super(Dep2pict, self).__init__(parent)

        # Set the flag d2p to True iff the external program dep2pict is installed.
        d2p = True
        try:
            sub=subprocess.run (["dep2pict", "--check"])
            if sub.returncode != 0:
                d2p = False
        except:
            d2p = False

        self.position = 0
        self.sentences = []
        self.offsets = []
        self.conll_file = None
        self.scroll_pos = None

        self.init_menu()
        self.init_watcher()
        self.init_central()

        if d2p:
            self.setWindowTitle('Dep2pict')

            self.setGeometry(0, 0, screen.width(), screen.height()/2)
            self.show()

            if len(sys.argv) > 1:
                self.open_new_file(sys.argv[1])
        else:
            self.message("The Dep2pict application requires the 'dep2pict' command\nSee http://dep2pict.loria.fr/installation for install instructions")
            qApp.quit()


    def init_watcher(self):
        self.watcher = QFileSystemWatcher()
        self.watcher.fileChanged.connect(self.watcher_action)

    def watcher_action(self):
        qpoint = self.web_view.page().scrollPosition()
        self.scroll_pos = (qpoint.x(), qpoint.y())
        self.data_refresh()

    def init_central(self):
        self.central = QWidget()
        self.setCentralWidget(self.central)

        # The [vbox] covering the whole interface
        vbox = QVBoxLayout()
        self.central.setLayout(vbox)

        # Horizontal [splitter]
        splitter = QSplitter(Qt.Horizontal)
        vbox.addWidget(splitter)

        # a treeview [self.data_view] on the left side of [splitter]
        self.data_view = MyTreeView()
        splitter.addWidget(self.data_view)

        # Add the home-made redraw event and bind it
        self.data_view.c = Communicate()
        self.data_view.c.redraw.connect(self.redraw)

        # build [self.model] and bind it to [self.data_view]
        self.model = QStandardItemModel(0, 1, self)
        self.model.setHeaderData(0, Qt.Horizontal, "Sent_id")
        self.data_view.setModel(self.model)

        # [right_vbox] as the right side of the [splitter]
        right_widget = QWidget()
        splitter.addWidget(right_widget)
        splitter.setStretchFactor(1, 10)
        right_vbox = QVBoxLayout()
        right_widget.setLayout(right_vbox)

        # [self.text_label] for sentence display
        self.text_label = QLabel("")
        self.text_label.setFont(QFont('SansSerif', 24))
        self.text_label.setHidden(True)
        self.text_label.setWordWrap(True);
        right_vbox.addWidget(self.text_label)

        # [right_hbox] for sentence + slider
        right_hbox = QHBoxLayout()
        right_hbox.setContentsMargins(0,0,0,0) #(left, top, right, bottom)
        right_vbox.addLayout(right_hbox)

        # [self.web_view] for dependency display
        self.web_view = QtWebEngineWidgets.QWebEngineView(self)
        right_hbox.addWidget(self.web_view)
        self.web_view.loadFinished.connect(self.post_draw) #keep scroll position

        # add [slider] and connect it to [self.web_view]
        slider = QSlider(Qt.Vertical)
        slider.setMaximum(300)
        slider.setMinimum(50)
        slider.setValue(100)
        slider.valueChanged.connect(lambda v:self.web_view.setZoomFactor(v/100))
        right_hbox.addWidget(slider)

    def init_menu(self):
        bar = self.menuBar()
        file = bar.addMenu("File")
        file.triggered[QAction].connect(self.menu_file_action)

        open_ = QAction("Open",self)
        open_.setShortcut("Ctrl+O")
        file.addAction(open_)

        quit = QAction("Quit",self)
        quit.setShortcut("Ctrl+Q")
        file.addAction(quit)

    def menu_file_action(self, q):
        action=q.text()
        if action == "Quit":
            qApp.quit()
        if action == "Open":
            self.open_dialog()

    def open_dialog(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file')

        if fname[0]:
            self.open_new_file(fname[0])

    def update_watcher(self):
        if self.watcher.files() != []:
            self.watcher.removePaths (self.watcher.files());
        if self.conll_file:
            self.watcher.addPath(self.conll_file);

    def redraw(self):
        try:
            index = self.data_view.current_index
            # http://doc.qt.io/qt-5/qstandarditem.html
            new_position = index.model().itemFromIndex(index).row()
            if self.position != new_position:
                self.position = new_position
                self.scroll_pos = None
                self.draw()
        except:
            pass

    def draw (self):
        try:
            sentence = self.sentences[self.position]
        except IndexError:
            self.message('Fewer sentences, jump to the first one')
            self.position = 0
            sentence = self.sentences[self.position]
        reply = conll.to_svg (sentence)
        if os.path.isfile(reply):
            self.web_view.setUrl(QUrl("file://"+reply))
        else:
            err = json.loads(reply)
            err["file"] = self.conll_file
            if "line" in err:
                err["line"] = err["line"] + self.offsets[self.position]
            html = json2html.convert(json = err)
            self.web_view.setHtml("<h1>Error in CoNLL data:</h1>\n"+html)
        text = conll.get_text(sentence)
        if text is None:
            self.text_label.setHidden(True)
        else:
            self.text_label.setHidden(False)
            self.text_label.setText(text)

    def post_draw(self):
        if self.scroll_pos != None:
            self.web_view.page().runJavaScript("window.scrollTo(%g, %g);" % self.scroll_pos)

    def open_new_file(self, filename):
        self.conll_file = filename
        self.setWindowTitle('Dep2pict -- '+filename)
        self.position = 0
        self.scroll_pos = None
        self.update_watcher()
        self.data_refresh()

    def empty(self):
        self.web_view.setHtml("<h1>No graph</h1>")
        self.text_label.setHidden(True)

    def data_refresh(self):
        if self.conll_file:
            # Remove the current rows in self.model
            self.model.removeRows(0,self.model.rowCount ())
            try:
                (self.sentences, self.offsets) = conll.load_conll(self.conll_file)
                # Fill list
                pos=0
                conll.reset()
                for s in self.sentences:
                    self.model.insertRow(pos)
                    self.model.setData(self.model.index(pos, 0), conll.get_sentid (s))
                    pos += 1

                if self.sentences == []:
                    self.empty()
                    self.message('The file "%s" is empty' % self.conll_file)
                else:
                    # highlight the position in data_view
                    self.data_view.setCurrentIndex(self.model.index(self.position,0))
                    self.draw()
            except FileNotFoundError:
                self.empty()
                self.message('File not found: "%s"' % self.conll_file)

    def message(self,text):
        msgBox = QMessageBox(self.central)
        msgBox.setText(text)
        msgBox.exec_()


def main():
    import sys

    app = QApplication(sys.argv)
    screen = app.desktop().screenGeometry()
    Dep2pict(screen)
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
