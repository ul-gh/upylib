# -*- coding: utf-8 -*-
"""Monkey-patch sys.excepthook /inside/ a PyQt event, e.g. for handling
exceptions occuring in pyqtSlots.
"""
import sys
from traceback import format_exception
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMessageBox

def new_except_hook(etype, evalue, tb):
    QMessageBox.information(
        None, "Error", "".join(format_exception(etype, evalue, tb)))

def patch_excepthook():
    sys.excepthook = new_except_hook

TIMER = QTimer()
TIMER.setSingleShot(True)
TIMER.timeout.connect(patch_excepthook)
TIMER.start()

