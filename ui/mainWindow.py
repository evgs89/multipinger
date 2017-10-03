# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""

from PyQt5.QtCore import pyqtSlot,  pyqtSignal, QAbstractTableModel, QVariant, Qt, QModelIndex, QPoint
from PyQt5.QtWidgets import QMainWindow, QSystemTrayIcon, QHeaderView, QItemDelegate, QComboBox, QMenu
from PyQt5.QtGui import QIcon, QPixmap, QBrush, QColor
from datetime import datetime
from .Ui_mainWindow import Ui_MainWindow
from ui.addAddress import addAddress
from ui.logView import logView
from ui.settings import Settings
from ui.browser import browser
import configparser,  subprocess, platform
from ui.extClasses import pinger

class loggingPinger(pinger):
    def __init__(self, address, timeout = 1, messages = None):
        pinger.__init__(self, address, timeout, messages)
        self.filename = 'logs/log_' + address + '.txt'
        self.__address = address

    def start(self, delay = 0):
        try:
            log = open(self.filename, 'x')
        except:
            log = open(self.filename, 'a')
        log.write('Control started at ' + datetime.now().strftime('%H:%M:%S %d/%m') + '\n')
        log.close()
        super().start(delay)
        
    def stop(self):
        try:
            log = open(self.filename, 'x')
        except:
            log = open(self.filename, 'a')
        log.write('Control stopped at ' + datetime.now().strftime('%H:%M:%S %d/%m') + '\n')
        log.close()
        super().stop()
        
    def stateChanged(self, state):
        try: log = open(self.filename, 'x')
        except: log = open(self.filename, 'a')
        if state: log.write(self.__address + ' is UP from ' + datetime.now().strftime('%H:%M:%S %d/%m') + '\n')
        else: log.write(self.__address + ' is DOWN from ' + datetime.now().strftime('%H:%M:%S %d/%m') + '\n')
        log.close()
        super().stateChanged(state)
        
    

class Model(QAbstractTableModel):
    notificator = pyqtSignal(str, str, bool)
    active = True
    def __init__(self, parent):
        QAbstractTableModel.__init__(self)
        self.gui = parent
        self.config = configparser.ConfigParser(allow_no_value = True)
        self.config.read('settings.ini')
        self.adresses = {}
        if 'ipList' in self.config:
            index = 0
            for i in self.config['ipList']:
                name = self.config[i]['name']
                p = loggingPinger(i)
                p.stateChangedSignal.connect(self.on_hostStateChanged)
                c = 0
                connectionMethod = self.config[i]['defaultAction']
                self.adresses[i] = [False, c, i, name, datetime.now(), p, index, connectionMethod]
                self.adresses[i][5].start()
                index += 1
        self.colLabels = [' ', 'c', 'ip', 'name', 'since', 'cnct']
            
    def rowCount(self, parent):
        return len(self.adresses)
    def columnCount(self, parent):
        return len(self.colLabels)
    def data(self, index, role):
        if not index.isValid(): return QVariant()
        elif role != Qt.DisplayRole and role != Qt.EditRole and role != Qt.BackgroundRole and role != Qt.DecorationRole: return QVariant()
        value = ''
        row = index.row()
        col = index.column()
        if role == Qt.DisplayRole:
            if col == 4: value = sorted(self.adresses.items(), key = lambda item: item[1][6])[row][1][4].strftime('%H:%M:%S') #возвращается объект типа datetime, потому надо его причесать
            elif col == 0: value = ''
            elif col == 5: value = sorted(self.adresses.items(), key = lambda item: item[1][6])[row][1][7]
            else: value = sorted(self.adresses.items(), key = lambda item: item[1][6])[row][1][col] #остальные объекты даём как есть
            return QVariant(value)
        if role == Qt.BackgroundRole:
            if sorted(self.adresses.items(), key = lambda item: item[1][6])[row][1][0]: color = QColor("#AAFFAA")
            else: color = QColor("#FFAAAA")
            background = QBrush(color)
            return QVariant(background)
        if role == Qt.DecorationRole and index.column() == 0:
            icon = QIcon()
            if sorted(self.adresses.items(), key = lambda item: item[1][6])[row][1][0]: icon.addPixmap(QPixmap(":/icons/success.png"))
            else: icon.addPixmap(QPixmap(":/icons/error.png"))
            return icon
        if role == Qt.EditRole and index.column() == 5:
            value = sorted(self.adresses.items(), key = lambda item: item[1][6])[row][1][7]
            return value
    def getRawData(self, index):
        if index < len(self.adresses):
            return sorted(self.adresses.items(), key = lambda item: item[1][6])[index][1]
    def setData(self, index, data, role):
        if role == Qt.EditRole and index.column() == 5:
            row = index.row()
            sorted(self.adresses.items(), key = lambda item: item[1][6])[row][1][7] = str(data)
    def setRawData(self, data):
        index = data['index']
        if data['ip'] in self.adresses:
            if self.adresses[data['ip']][3] != data['name']:
                self.adresses[data['ip']][3] = data['name']
                a = self.createIndex(index, 2)
                self.dataChanged.emit(a, a)
            elif self.adresses[data['ip']][7] != data['connection']:
                self.adresses[data['ip']][7] = data['connection']
                a = self.createIndex(index, 5)
                self.dataChanged.emit(a, a)
        else:
            p = loggingPinger(data['ip'])
            if index < len(self.adresses):
                oldIp = sorted(self.adresses.items(), key = lambda item: item[1][6])[index][0]##редактирование существующего адреса
                self.deleteRawData(oldIp)
                self.adresses[data['ip']] = [False, 0, data['ip'], data['name'], datetime.now(), p, index, data['connection']]
                a = self.createIndex(index, 0)
                b = self.createIndex(index, 6)
                self.dataChanged.emit(a, b)
            if index == len(self.adresses):
                self.adresses[data['ip']] = [False, 0, data['ip'], data['name'], datetime.now(), p, index, data['connection']]
                self.layoutChanged.emit()
            self.adresses[data['ip']][5].stateChangedSignal.connect(self.on_hostStateChanged)
            self.adresses[data['ip']][5].start()
        self.config['ipList'][data['ip']] = None
        self.config[data['ip']] = {}
        self.config[data['ip']]['name'] = data['name']
        self.config[data['ip']]['rdpLogin'] = data['login']
        self.config[data['ip']]['rdpPassword'] = data['pass']
        self.config[data['ip']]['defaultAction'] = data['connection']
        if data['notifyUp']: self.config[data['ip']]['notificationAtUp'] = 'True'
        else: self.config[data['ip']]['notificationAtUp'] = 'False'
        if data['notifyDown']: self.config[data['ip']]['notificationAtDown'] = 'True'
        else: self.config[data['ip']]['notificationAtDown'] = 'False'
        with open('settings.ini', 'w') as configfile: self.config.write(configfile)
    def deleteRawData(self, ip):
        indexDeleted = self.adresses[ip][6]
        self.adresses[ip][5].stop()
        self.adresses.pop(ip, None)
        self.config.remove_option('ipList', ip)
        self.config.remove_section(ip)
        with open('settings.ini', 'w') as configfile: self.config.write(configfile)
        return indexDeleted
    def deleteRow(self, index):
        ip = self.getRawData(index)[2]
        rowCount = len(self.adresses) - 1
        self.deleteRawData(ip)
        for i in range((index + 1), rowCount):
            key = self.getRawData(i)[2]
            self.adresses[key][6] -= 1
        self.layoutChanged.emit()
    def headerSettings(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.colLabels[section])
        return QVariant()
    def on_hostStateChanged(self, address, state):
        if address in self.adresses:
            self.adresses[address][0] = state
            self.adresses[address][4] = datetime.now()
            if state: self.adresses[address][1] += 1
            self.notificator.emit(address, self.adresses[address][3], state)
            row = self.adresses[address][6]
            a = self.createIndex(row, 0)
            b = self.createIndex(row, 4)
            self.dataChanged.emit(a, b)
    def flags(self, index):
        if index.column() == 5: return Qt.ItemIsEditable | Qt.ItemIsEnabled
        else: return Qt.ItemIsEnabled
    def readConfig(self):
        self.config.read('settings.ini')
    
class comboDelegate(QItemDelegate):
    def __init__(self, parent):
        QItemDelegate.__init__(self, parent)
    def createEditor(self, parent, option, index):
        combo = QComboBox(parent)
        li = []
        li.append("DEF")
        li.append("RDP")
        li.append("RA")
        li.append("IE")
        combo.addItems(li)
        return combo
        
    def setEditorData(self, editor, index):
        editor.setCurrentText(index.model().data(index, Qt.EditRole))
        
    def setModelData(self, editor, model, index):
        model.setData(index, editor.currentText(), Qt.EditRole)
        
    @pyqtSlot()
    def currentIndexChanged(self):
        self.commitData.emit(self.sender())



class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.checkSettings()
        self.Model = Model(self.tableView)
        self.tableView.setModel(self.Model)
        self.tableView.model().notificator.connect(self.notify)
        self.delegate = comboDelegate(self)
        self.tableView.setItemDelegateForColumn(5, self.delegate)
        self.tableView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tableView.customContextMenuRequested[QPoint].connect(self.contextMenuRequested)
        self.tableView.horizontalHeader().setSectionResizeMode(0, QHeaderView.Fixed)
        self.tableView.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.tableView.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.tableView.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self.tableView.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.tableView.horizontalHeader().setSectionResizeMode(5, QHeaderView.Fixed)
        self.tableView.horizontalHeader().setVisible(False)
        self.tableView.verticalHeader().setVisible(False)
        self.tableView.setColumnWidth(0, 23)
        self.tableView.setColumnWidth(5, 55)
        self.programIcon = QIcon()
        self.programIcon.addPixmap(QPixmap(":/icons/paperplane.png"))
        self.trayIcon = QSystemTrayIcon(self.programIcon)
        self.trayIcon.show()
        self.settingsChanged()
    def settingsChanged(self):
        config = configparser.ConfigParser(allow_no_value = True)
        config.read('settings.ini')
        self.tableView.model().readConfig()
        if 'otherSettings' in config:
            if config['otherSettings']['showCount'] == 'False': self.tableView.setColumnHidden(1, True)
            else: self.tableView.setColumnHidden(1, False)
            if config['otherSettings']['showName'] == 'False': self.tableView.setColumnHidden(3, True)
            else: self.tableView.setColumnHidden(3, False)
    def checkSettings(self):        
        config = configparser.ConfigParser(allow_no_value = True)
        config.read('settings.ini')
        changed = False
        for i in config['ipList']:
            if i not in config.sections():
                config[i] = {}
                config[i]['name'] = ''
                config[i]['rdplogin'] = config['otherSettings']['defaultLogin']
                config[i]['rdppassword'] = config['otherSettings']['defaultPassword']
                config[i]['defaultaction'] = 'DEF'
                config[i]['notificationatup'] = config['otherSettings']['defaultNotificationAtUp']
                config[i]['notificationatdown'] = config['otherSettings']['defaultNotificationAtDown']
                changed = True
        if changed: 
            with open('settings.ini', 'w') as configfile: config.write(configfile)
            changed = False

    def contextMenuRequested(self, point):
        contextMenu = QMenu(self)
        removeIcon = QIcon()
        removeIcon.addPixmap(QPixmap(":/icons/minus.png"))
        removeAction = contextMenu.addAction(removeIcon, "Remove")
        removeAction.triggered.connect(self.deleteItemFromTableView)
        editIcon = QIcon()
        editIcon.addPixmap(QPixmap(":/icons/edit.png"))
        editAction = contextMenu.addAction(editIcon, "Edit")
        editAction.triggered.connect(self.editItemFromTableView)
        viewLog = QIcon()
        viewLog.addPixmap(QPixmap(":/icons/log.png"))
        viewLogAction = contextMenu.addAction(viewLog, "View log")
        viewLogAction.triggered.connect(self.viewLogFromTableView)
        contextMenu.exec_(self.mapToGlobal(point))
                
    @pyqtSlot()
    def deleteItemFromTableView(self):
        indexRow = self.tableView.currentIndex().row()
        self.tableView.model().deleteRow(indexRow)
        

    @pyqtSlot()
    def editItemFromTableView(self):
        self.setWin = addAddress(self)
        indexRow = self.tableView.currentIndex().row()
        data = self.tableView.model().getRawData(indexRow)
        self.setWin.indexRow = indexRow
        self.setWin.ipAddress.setText(data[2])
        config = configparser.ConfigParser(allow_no_value = True)
        config.read('settings.ini')
        self.setWin.name.setText(config[data[2]]['name'])
        self.setWin.rdpLogin.setText(config[data[2]]['rdpLogin'])
        self.setWin.rdpPassword.setText(config[data[2]]['rdpPassword'])
        a = {'DEF':0, 'RDP':1, 'RA':2, 'IE':3}
        self.setWin.comboBox.setCurrentIndex(a[config[data[2]]['defaultAction']])
        self.setWin.notifyAtUp.setChecked(config.getboolean(data[2], 'notificationAtUp'))
        self.setWin.notifyAtDown.setChecked(config.getboolean(data[2], 'notificationAtDown'))
        self.setWin.show()
        
    @pyqtSlot()
    def viewLogFromTableView(self):
        indexRow = self.tableView.currentIndex().row()
        data = self.tableView.model().getRawData(indexRow)
        filename = 'logs/log_' + data[2] + '.txt'
        self.logViewer = logView(self)
        self.logViewer.filename = filename
        text = ''
        try: 
            log = open(filename,  'r')
            text = log.read()
            log.close()
        except: text = ''
        if text == '': text = 'Log is empty'
        self.logViewer.log.setPlainText(text)
        self.logViewer.show()
    
    @pyqtSlot()
    def on_settingsButton_clicked(self):
        self.confWin = Settings(self)
        self.confWin.show()

    
    @pyqtSlot(dict)
    def on_addAddress(self, data):
        self.tableView.model().setRawData(data)

    
    @pyqtSlot()
    def on_btnAddAddress_clicked(self):
        self.setWin = addAddress(self)
        self.setWin.indexRow = self.tableView.model().rowCount(self)
        config = configparser.ConfigParser(allow_no_value = True)
        config.read('settings.ini')
        if 'otherSettings' in config:
            self.setWin.ipAddress.setText(config['otherSettings']['defaultIp'])
            self.setWin.rdpLogin.setText(config['otherSettings']['defaultLogin'])
            self.setWin.rdpPassword.setText(config['otherSettings']['defaultPassword'])
            a = {'DEF':0, 'RDP':1, 'RA':2, 'IE':3}
            self.setWin.comboBox.setCurrentIndex(a[config['otherSettings']['default']])
            self.setWin.notifyAtUp.setChecked(config.getboolean('otherSettings', 'defaultNotificationAtUp'))
            self.setWin.notifyAtDown.setChecked(config.getboolean('otherSettings', 'defaultNotificationAtDown'))
        self.setWin.show()
    
    def notify(self, ip, name, state):
        text = ip
        if name != '': text += ' (' + name + ')'
        if state: text += ' is UP'
        else: text += ' is DOWN'
        self.statusMessage.setText(text)
        config = configparser.ConfigParser(allow_no_value = True)
        config.read('settings.ini')
        if state and config.getboolean(ip, 'notificationAtUp'): self.trayIcon.showMessage(ip, text)
        if not state and config.getboolean(ip, 'notificationAtDown'): self.trayIcon.showMessage(ip, text)
    
    @pyqtSlot(QModelIndex)
    def on_tableView_doubleClicked(self, index):
        if index.column() != 5:
            indexRow = index.row()
            conIP = str(self.tableView.model().getRawData(indexRow)[2])
            method = self.tableView.model().getRawData(indexRow)[7]
            config = configparser.ConfigParser(allow_no_value = True)
            config.read('settings.ini')
            self.rdp = ''
            self.ra = ''
            pathfile = open('paths.ini',  'r')
            for line in pathfile:
                if line[:4] == 'rdp=' or line[:4] == 'RDP=': self.rdp = line[4:]
                if line[:3] == 'ra=' or line[:3] == 'RA=': self.ra = line[3:]
                if line[:3] == 'ie=' or line[:3] == 'IE=': self.ie = line[3:]
            if method == 'DEF': method = config['otherSettings']['default']
            if method == 'RDP': 
                self.rdpConnection(conIP)
            elif method == 'RA': 
                self.radminConnection(conIP)
            elif method == 'IE':
                self.browserConnection(conIP)
    
    def rdpConnection(self, host):
        config = configparser.ConfigParser(allow_no_value = True)
        config.read('settings.ini')
        if  platform.system().lower()=="windows":
            if len(self.rdp) > 5: ##чтобы не париться, если при разборе попадут пробелы или перевод строки
                command = self.rdp[:-1]
            else:
                command1 = 'cmdkey /delete:' + host
                command2 = 'cmdkey /add:' + host + ' /user:' + config[host]['rdplogin'] + ' /pass:' + config[host]['rdppassword']
                command3 = 'mstsc /v:' + host
                if config.getboolean('rdpSettings', 'fullscreen'): command3 += ' /f'
                else: command3 += ' /w:' + config['rdpSettings']['width'] + ' /h:' + config['rdpSettings']['heigth']
                subprocess.Popen(command1, shell = True) ##os.system(command1)
                subprocess.Popen(command2, shell = True) ##os.system(command2)
                subprocess.Popen(command3, shell = True) ##os.system(command3)
        else:
            command = 'xfreerdp'
            command += ' /u:' + config[host]['rdplogin'] + ' /p:' + config[host]['rdppassword']
            command += ' /t:' + host + ' /v:' + host + ' /w:' + config['rdpSettings']['width'] + ' /h:' + config['rdpSettings']['heigth'] + ' /bpp:' + config['rdpSettings']['colordepth']
            if config.getboolean('rdpSettings', 'fullscreen'): command += ' /f'
            if config.getboolean('rdpSettings', 'compression'): command += ' +compression'
            if config.getboolean('rdpSettings', 'audio'): command += ' /audio-mode'
            if config.getboolean('rdpSettings', 'clipboard'): command += ' +clipboard'
            if not config.getboolean('rdpSettings', 'themes'): command += ' -themes'
            if not config.getboolean('rdpSettings', 'wallpaper'): command += ' -wallpaper'
            print(command)
            subprocess.Popen(command, shell = True)
        
    def radminConnection(self, host):
        config = configparser.ConfigParser(allow_no_value = True)
        config.read('settings.ini')
        command = self.ra[:-1]
        command += ' /connect:' + host + ':' + config['radminSettings']['port'] + ' /' + config['radminSettings']['colordepth'] + 'bpp /updates:' + config['radminSettings']['updates']
        if config.getboolean('radminSettings', 'fullscreen'): command += ' /fullscreen'
        subprocess.Popen(command, shell = True) ##os.system(command)

    def browserConnection(self, host):
        config = configparser.ConfigParser(allow_no_value = True)
        config.read('settings.ini')
        if config['otherSettings']['browser'] == 'internal':
            webBrowser = browser(self)
            webBrowser.urlEdit.setText(host)
            webBrowser.urlEdit.returnPressed.emit()
            webBrowser.show()
        else:
            if  platform.system().lower()=="windows" and config['otherSettings']['browser'] == 'midori':
                if len(self.ie) > 5: ##чтобы не париться, если при разборе попадут пробелы или перевод строки
                    command = self.ie[:-1]
                    arg = "-a " + host
            elif config['otherSettings']['browser'] == 'midori':
                command = 'midori'
                arg = "-a " + host
            else:
                    command = config['otherSettings']['browser']
                    arg = host
            print(command, '', arg)
            subprocess.Popen((command + ' ' + arg), shell = True)##os.system(command)
        
    @pyqtSlot()
    def closeEvent(self, event):
        for i in self.tableView.model().adresses:
            self.tableView.model().adresses[i][5].stop()
        self.trayIcon.hide()
        event.accept()
