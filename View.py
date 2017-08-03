#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generic Test App
"""
import copy
import os
import traceback
import converter

from PyQt5 import QtWidgets, uic, QtCore, QtGui
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QKeySequence
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot, QEvent, QSize, QFile, QTextStream, QIODevice, QDir
from PyQt5.QtWidgets import QBoxLayout, QSpinBox, QDoubleSpinBox, QSlider, QLabel, QWidget, QHBoxLayout, \
    QVBoxLayout, QStackedWidget, QComboBox, QSizePolicy, QToolButton, QMenu, QAction, QMessageBox, QApplication, \
    QScrollArea, QFrame, QGridLayout, QSplitter, QCheckBox, QSpacerItem, QLineEdit, QPushButton, QFormLayout, QDialog

__authors__ = {"Philipp Reichert": "prei@me.com"}

try:
    mainView_path = os.path.join('MainView.ui')
    base, form = uic.loadUiType(mainView_path)
except FileNotFoundError:
    raise NameError(os.listdir(os.curdir))


class MainWindow(base, form):
    def __init__(self, parent=None):
        super(base, self).__init__(parent)

        self.remote = True
        self.icon = QIcon(os.path.join('.', 'pr-logo-white2.ico'))
        self.openLocalAct = QAction("&Open local HTML", self, shortcut="Ctrl+O",
                                    triggered=self.set_input_file)
        self.openURLAct = QAction("&Open URL HTML ", self, shortcut="Ctrl+U",
                                  triggered=self.set_input_url)
        self.openLocalActDir = QAction("&Open Directory", self, shortcut="Ctrl+D",
                                       triggered=self.set_input_dir)
        self.saveAct = QAction("&Save PDF", self, shortcut="Ctrl+S",
                               triggered=self.set_output_file)
        self.saveActDir = QAction("&Output Directory", self, shortcut="Ctrl+L",
                                  triggered=self.set_output_dir)
        self.docsAct = QAction("&Documentation", self, triggered=self.open_docs)
        self.aboutAct = QAction("&About HTML-Converter", self, triggered=self.about)
        self.exitAct = QAction("&Exit", self, shortcut="Ctrl+Q",
                               triggered=self.close)
        self.helpMenu = QMenu("&Help", self)
        self.fileMenu = QMenu("&File", self)

        self.saveAct.setEnabled(False)
        self.saveActDir.setEnabled(False)

        self.dialog = QtWidgets.QDialog()
        self.dialog.setWindowTitle("HTML URL")
        self.dialog.setWindowIcon(self.icon)
        self.layout = QVBoxLayout()
        self.dialog.setLayout(self.layout)

        self.lineInput = QLineEdit()
        self.lineInput.setObjectName("URL")
        self.lineInput.setText("")

        self.button = QPushButton()
        self.button.setText("OK")

        self.layout.addWidget(self.lineInput)
        self.layout.addWidget(self.button)

        self.button.clicked.connect(self.get_text)

        self.setupUi(self)

        self.input_f = ''
        self.input_url = ''
        self.output_f = ''
        self.input_d = ''
        self.output_d = ''

        self.createMenus()
        self.draw_ui()

    def createMenus(self):

        # &File
        self.fileMenu.addAction(self.openLocalAct)
        self.fileMenu.addAction(self.openURLAct)
        self.fileMenu.addAction(self.saveAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.openLocalActDir)
        self.fileMenu.addAction(self.saveActDir)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAct)

        # &Help
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.docsAct)

        self.menuBar().addMenu(self.fileMenu)
        self.menuBar().addMenu(self.helpMenu)

    def about(self):

        try:
            html_file = os.path.join(os.getcwd(), 'about.html')
            f = QFile(html_file)
            f.open(QIODevice.ReadOnly)
            reader = QTextStream(f)
            reader.setCodec("UTF-8")
            text = reader.readAll()
        except FileNotFoundError:
            print("about.html could not be opened")
            return

        QMessageBox.about(self, "About HTML-Converter", text)

    def open_docs(self):
        try:
            html_file = os.path.join(os.getcwd(), 'documentation.html')
            f = QFile(html_file)
            f.open(QIODevice.ReadOnly)
            reader = QTextStream(f)
            reader.setCodec("UTF-8")
            text = reader.readAll()
        except FileNotFoundError:
            print("about.html could not be opened")
            return

        QMessageBox.about(self, "PDFreactor documentation", text)

    def print_(self):
        pass

    def draw_ui(self):
        """
        This function draws all additional UI elements. If you want the
        application to display any additional things like a button you can
        either add it in the QtDesigner or declare it here.
        """
        self.setWindowTitle("HTML-Converter")
        self.setWindowIcon(self.icon)
        # self.setWindowFlags(Qt.FramelessWindowHint)

        # self.setStyleSheet("QScrollBar:horizontal {max-height: 15px;}" "QScrollBar:vertical {max-width: 15px;}")

        # self.mid_panel.setStyleSheet("border:0;")
        # self.right_panel.setStyleSheet("border:0;")

    @pyqtSlot()
    def set_input_file(self):
        """
        This method sets the url for the input html.
        """
        self.input_f = QtWidgets.QFileDialog.getOpenFileName(self, 'Open HTML', '', 'HTML (*.HTML)')
        if self.input_f[0]:
            print("Input file: " + str(self.input_f[0]))
            self.saveAct.setEnabled(True)
            self.remote = False

    def get_text(self):
        self.input_url = self.lineInput.text()
        if self.input_url:
            print("Input file: " + self.input_url)
            self.saveAct.setEnabled(True)
            self.remote = True

        self.dialog.hide()

    @pyqtSlot()
    def set_input_url(self):
        """
        This method sets the url for the input html.
        """

        self.dialog.show()

    @pyqtSlot()
    def set_input_dir(self):
        self.input_d = QtWidgets.QFileDialog.getExistingDirectory(self, 'Open Folder containing HTML files', '.')
        if self.input_d:
            print("Input directory: " + str(self.input_d))
            self.saveActDir.setEnabled(True)

    @pyqtSlot()
    def set_output_file(self):
        """
        This method sets saves the converted file.
        """

        self.output_f = QtWidgets.QFileDialog.getSaveFileName(self, "Save PDF", '', 'PDF file (*.pdf)')
        try:
            if self.output_f:
                print("Output file: " + self.output_f[0])
        except Exception as e:
            print("Failed to save pdf file on file system")
            traceback.print_exc()
            return

        if self.output_f and self.input_f:
            if not self.remote:
                converter.convert(str(self.input_f[0]), self.output_f[0])
            else:
                converter.convert(self.input_url, self.output_f[0], self.remote)
            self.saveAct.setEnabled(False)
            self.output_f = ''

    @pyqtSlot()
    def set_output_dir(self):
        self.output_d = QtWidgets.QFileDialog.getExistingDirectory(self, 'Save Folder for converted PDF files', '.')
        if self.output_d:
            print("Output directory: " + str(self.output_d))
            self.saveActDir.setEnabled(True)

            converter.convert_batch(self.input_d, self.output_d)
            self.saveActDir.setEnabled(False)
            self.output_d = ''


if __name__ == '__main__':
    pass
