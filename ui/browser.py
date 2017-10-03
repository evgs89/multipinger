# -*- coding: utf-8 -*-

"""
Module implementing browser.
"""

from PyQt5.QtCore import pyqtSlot, QUrl
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from PyQt5 import QtWebKitWidgets, QtNetwork

from .Ui_browser import Ui_browserWindow


class browser(QMainWindow, Ui_browserWindow):
    def __init__(self, parent=None):
        super(browser, self).__init__(parent)
        self.setupUi(self)
        self.webView = QtWebKitWidgets.QWebView()
        self.webView.setObjectName("webView")
        self.netManager = QtNetwork.QNetworkAccessManager()
        self.webView.page().setNetworkAccessManager(self.netManager)
        self.verticalLayout.addWidget(self.webView)
        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 20)
        self.urlEdit.returnPressed.connect(self.on_goButton_released)
        self.webView.loadFinished.connect(self.on_webView_titleChanged)
        self.webView.loadFinished.connect(self.on_webView_urlChanged)
        self.webView.page().setForwardUnsupportedContent(True)
        self.webView.page().downloadRequested.connect(self.on_downloadRequest)
        self.webView.page().unsupportedContent.connect(self.on_unsupportedContent)
    
    @pyqtSlot()
    def on_goButton_released(self):
        theUrl = QUrl.fromUserInput(self.urlEdit.text())
        self.webView.load(theUrl)
    
    @pyqtSlot()
    def on_goBack_released(self):
        self.webView.back()
    
    @pyqtSlot()
    def on_goForward_released(self):
        self.webView.forward()
    
    @pyqtSlot()
    def on_webView_titleChanged(self):
        self.setWindowTitle(self.webView.title())
    
    @pyqtSlot()
    def on_webView_urlChanged(self):
        self.urlEdit.setText(self.webView.url().toString())
    
    def on_downloadRequest(self, request):
        self.request = request
        self.download()

    def on_unsupportedContent(self, reply):
        self.request = reply.request()
        self.request.setUrl(reply.url())
        self.download()        
    
    def download(self):
        self.reply = self.netManager.get(self.request)
        defFilename = self.request.url().path().split('/')[-1]
        self.filename = QFileDialog.getSaveFileName(self, 'Save', defFilename)
        if not self.filename[0]: return
        else:
            with open(self.filename[0], 'wb') as f:
                f.write(self.reply.readAll())
                f.close()
                print(self.filename[0])
            self.filename = ''
