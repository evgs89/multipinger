# -*- coding: utf-8 -*-

"""
Module implementing logView.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog

from .Ui_logView import Ui_Dialog


class logView(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        super(logView, self).__init__(parent)
        self.setupUi(self)
        self.filename = ''
    
    @pyqtSlot()
    def on_clear_released(self):
        log = open(self.filename, 'w')
        log.write('')
        log.close()
        self.log.setPlainText('')
