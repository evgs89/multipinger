# -*- coding: utf-8 -*-

"""
Module implementing Settings.
"""

from PyQt5.QtCore import pyqtSlot, pyqtSignal, Qt
from PyQt5.QtWidgets import QDialog
import configparser

from .Ui_settings import Ui_Settings


class Settings(QDialog, Ui_Settings):
    settingsChanged = pyqtSignal()
    def __init__(self, parent=None):
        super(Settings, self).__init__(parent)
        self.setupUi(self)
        self.setWindowModality(Qt.WindowModal)
        self.settingsChanged.connect(parent.settingsChanged)
        self.config = configparser.ConfigParser(allow_no_value = True)
        self.config.read('settings.ini')
        self.rdp = ''
        self.ra = ''
        self.ie=''
        pathfile = open('paths.ini',  'r')
        for line in pathfile:
            if line[:4] == 'rdp=' or line[:4] == 'RDP=': self.rdp = line[4:]
            if line[:3] == 'ra=' or line[:3] == 'RA=': self.ra = line[3:]
            if line[:3] == 'ie=' or line[:3] == 'IE=': self.ie = line[3:]
        #Program Settings reading
        self.defaultIp.setText(self.config['otherSettings']['defaultip'])
        a = {'RDP':0, 'RA':1, 'IE':2}
        self.comboBox.setCurrentIndex(a[self.config['otherSettings']['default']])
        self.defaultRdpLogin.setText(self.config['otherSettings']['defaultlogin'])
        self.defaultRdpPassword.setText(self.config['otherSettings']['defaultpassword'])
        self.showName.setChecked(self.config.getboolean('otherSettings', 'showname'))
        self.showCount.setChecked(self.config.getboolean('otherSettings', 'showcount'))
        self.notifyAtUp.setChecked(self.config.getboolean('otherSettings', 'defaultNotificationAtUp'))
        self.notifyAtDown.setChecked(self.config.getboolean('otherSettings', 'defaultNotificationAtDown'))
        #RDP settings reading
        self.width.setEditText(self.config['rdpSettings']['width'])
        self.heigth.setEditText(self.config['rdpSettings']['heigth'])
        self.pathXRDP.setText(self.rdp)
        b = {'15':0, '16':1, '24':2, '32':3}
        self.comboBox_4.setCurrentIndex(b[self.config['rdpSettings']['colordepth']])
        self.fullscreen.setChecked(self.config.getboolean('rdpSettings', 'fullscreen'))
        self.compression.setChecked(self.config.getboolean('rdpSettings', 'compression'))
        self.audio.setChecked(self.config.getboolean('rdpSettings', 'audio'))
        self.clipboard.setChecked(self.config.getboolean('rdpSettings', 'clipboard'))
        self.themes.setChecked(self.config.getboolean('rdpSettings', 'themes'))
        self.wallpaper.setChecked(self.config.getboolean('rdpSettings', 'wallpaper'))
        #RAdmin settings
        self.lineEdit.setText(self.config['radminSettings']['port'])
        c = {'24':0, '16':1, '8':2, '4':3, '2':4, '1':5}
        self.colorDepthRA.setCurrentIndex(c[self.config['radminSettings']['colordepth']])
        self.updates.setValue(int(self.config['radminSettings']['updates']))
        self.lineEdit_3.setText(self.ra)
        self.fullscreenRA.setChecked(self.config.getboolean('radminSettings', 'fullscreen'))
        #IE settings
        self.midoriPath.setText(self.ie)
        d = {'internal':0,  'midori':1,  'firefox':2}
        if (self.config['otherSettings']['browser']) in d.keys():
            index = d[self.config['otherSettings']['browser']]
            self.browser.setCurrentIndex(index)
        else:
            self.browser.addItem(self.config['otherSettings']['browser'])
            self.browser.setCurrentIndex(3)
        #
        self.tabWidget.setCurrentIndex(0)
        #

    
    @pyqtSlot()
    def on_buttonBox_accepted(self):
        #main settings
        self.config['otherSettings']['defaultip'] = self.defaultIp.text()
        self.config['otherSettings']['default'] = self.comboBox.currentText()
        self.config['otherSettings']['defaultlogin'] = self.defaultRdpLogin.text()
        self.config['otherSettings']['defaultpassword'] = self.defaultRdpPassword.text()
        self.config['otherSettings']['showname'] = str(self.showName.isChecked())
        self.config['otherSettings']['showcount'] = str(self.showCount.isChecked())
        self.config['otherSettings']['defaultNotificationAtUp'] = str(self.notifyAtUp.isChecked())
        self.config['otherSettings']['defaultNotificationAtDown'] = str(self.notifyAtDown.isChecked())
        #RDP
        self.config['rdpSettings']['width'] = self.width.currentText()
        self.config['rdpSettings']['heigth'] = self.heigth.currentText()
        self.rdp = self.pathXRDP.text()
        self.config['rdpSettings']['colordepth'] = self.comboBox_4.currentText()
        self.config['rdpSettings']['fullscreen'] = str(self.fullscreen.isChecked())
        self.config['rdpSettings']['compression'] = str(self.compression.isChecked())
        self.config['rdpSettings']['audio'] = str(self.audio.isChecked())
        self.config['rdpSettings']['clipboard'] = str(self.clipboard.isChecked())
        self.config['rdpSettings']['themes'] = str(self.themes.isChecked())
        self.config['rdpSettings']['wallpaper'] = str(self.wallpaper.isChecked())
        #RAdmin settings
        self.config['radminSettings']['port'] = self.lineEdit.text()
        self.config['radminSettings']['colordepth'] = self.colorDepthRA.currentText()
        self.config['radminSettings']['updates'] = str(self.updates.value())
        self.ra = self.lineEdit_3.text()
        self.config['radminSettings']['fullscreen'] = str(self.fullscreenRA.isChecked())
        #IE settings
        self.config['otherSettings']['browser'] = self.browser.currentText()
        self.ie = self.midoriPath.text()
        #save settings to file
        lines = []
        lines.append('rdp=' + self.rdp + '\n')
        lines.append('ra=' + self.ra + '\n')
        lines.append('ie=' + self.ie + '\n')
        settingsFile = open('paths.ini',  'w')
        settingsFile.writelines(lines)
        settingsFile.close()
        with open('settings.ini', 'w') as configfile: self.config.write(configfile)
        self.settingsChanged.emit()
        self.close()
    
    @pyqtSlot()
    def on_buttonBox_rejected(self):
        self.close()
