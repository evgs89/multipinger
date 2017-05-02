# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/es89/Dropbox/Projects/Python/MultiPing_v2/ui/browser.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_browserWindow(object):
    def setupUi(self, browserWindow):
        browserWindow.setObjectName("browserWindow")
        browserWindow.resize(800, 600)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(browserWindow.sizePolicy().hasHeightForWidth())
        browserWindow.setSizePolicy(sizePolicy)
        browserWindow.setMinimumSize(QtCore.QSize(300, 150))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/worldwide.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        browserWindow.setWindowIcon(icon)
        self.centralWidget = QtWidgets.QWidget(browserWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralWidget.sizePolicy().hasHeightForWidth())
        self.centralWidget.setSizePolicy(sizePolicy)
        self.centralWidget.setMinimumSize(QtCore.QSize(300, 150))
        self.centralWidget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.centralWidget.setObjectName("centralWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralWidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.urlEdit = QtWidgets.QLineEdit(self.centralWidget)
        self.urlEdit.setObjectName("urlEdit")
        self.horizontalLayout_2.addWidget(self.urlEdit)
        self.goButton = QtWidgets.QPushButton(self.centralWidget)
        self.goButton.setMinimumSize(QtCore.QSize(30, 0))
        self.goButton.setMaximumSize(QtCore.QSize(50, 16777215))
        self.goButton.setObjectName("goButton")
        self.horizontalLayout_2.addWidget(self.goButton)
        self.goBack = QtWidgets.QPushButton(self.centralWidget)
        self.goBack.setMinimumSize(QtCore.QSize(30, 0))
        self.goBack.setMaximumSize(QtCore.QSize(50, 16777215))
        self.goBack.setObjectName("goBack")
        self.horizontalLayout_2.addWidget(self.goBack)
        self.goForward = QtWidgets.QPushButton(self.centralWidget)
        self.goForward.setMinimumSize(QtCore.QSize(30, 0))
        self.goForward.setMaximumSize(QtCore.QSize(50, 16777215))
        self.goForward.setObjectName("goForward")
        self.horizontalLayout_2.addWidget(self.goForward)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout.addLayout(self.verticalLayout)
        browserWindow.setCentralWidget(self.centralWidget)

        self.retranslateUi(browserWindow)
        QtCore.QMetaObject.connectSlotsByName(browserWindow)

    def retranslateUi(self, browserWindow):
        _translate = QtCore.QCoreApplication.translate
        browserWindow.setWindowTitle(_translate("browserWindow", "MainWindow"))
        self.goButton.setText(_translate("browserWindow", "GO!"))
        self.goBack.setText(_translate("browserWindow", "<="))
        self.goForward.setText(_translate("browserWindow", "=>"))

import ui.icons_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    browserWindow = QtWidgets.QMainWindow()
    ui = Ui_browserWindow()
    ui.setupUi(browserWindow)
    browserWindow.show()
    sys.exit(app.exec_())

