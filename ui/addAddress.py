# -*- coding: utf-8 -*-

"""
Module implementing addAddress.
"""

from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QDialog

from .Ui_addAddress import Ui_Dialog


class addAddress(QDialog, Ui_Dialog):
    addedAddress = pyqtSignal(dict)
    indexRow = 0
    
    def __init__(self, parent):
        super(addAddress, self).__init__(parent)
        self.setupUi(self)
        self.addedAddress.connect(parent.on_addAddress)
        self.data = []
    
    @pyqtSlot()
    def on_buttonBox_accepted(self):
        a = {0:'DEF', 1:'RDP', 2:'RA', 3:'IE'}
        self.data = {'index':self.indexRow, 'ip':self.ipAddress.text(), 'name':self.name.text(), 'login':self.rdpLogin.text(), 'pass':self.rdpPassword.text(), 'connection':a[self.comboBox.currentIndex()], 'notifyUp':self.notifyAtUp.isChecked(), 'notifyDown':self.notifyAtDown.isChecked()}
        self.addedAddress.emit(self.data)
        self.close()
    
    @pyqtSlot()
    def on_buttonBox_rejected(self):
        self.close()
