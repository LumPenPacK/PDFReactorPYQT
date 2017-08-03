#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
The main nefi2 startup script.
It loads extension loader and initializes UI.
It also enables console batch processing mode.
"""
import os

import View

import sys
import ctypes
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication
import qdarkstyle

__authors__ = {"Philipp Reichert": "prei@me.com"}


class Main:
    @staticmethod
    def gui_mode():
        app_id = 'Test App'  # arbitrary string
        if sys.platform == 'win32' or sys.platform == 'win64':
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)

        app = QApplication(sys.argv)
        app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        app.setQuitOnLastWindowClosed(True)
        #app.setWindowIcon(QtGui.QIcon(os.path.join('path', 'file.ico')))
        wnd = View.MainWindow()
        wnd.show()
        sys.exit(app.exec_())


if __name__ == '__main__':
    Main.gui_mode()
