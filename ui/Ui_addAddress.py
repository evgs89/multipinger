# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/es89/Dropbox/Projects/Python/MultiPing_v2/ui/addAddress.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowModality(QtCore.Qt.WindowModal)
        Dialog.resize(323, 233)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/plus.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        Dialog.setSizeGripEnabled(True)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(0, 200, 321, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.layoutWidget = QtWidgets.QWidget(Dialog)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 0, 311, 200))
        self.layoutWidget.setObjectName("layoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.layoutWidget)
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.layoutWidget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.ipAddress = QtWidgets.QLineEdit(self.layoutWidget)
        self.ipAddress.setObjectName("ipAddress")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.ipAddress)
        self.label_2 = QtWidgets.QLabel(self.layoutWidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.name = QtWidgets.QLineEdit(self.layoutWidget)
        self.name.setText("")
        self.name.setObjectName("name")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.name)
        self.label_3 = QtWidgets.QLabel(self.layoutWidget)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.rdpLogin = QtWidgets.QLineEdit(self.layoutWidget)
        self.rdpLogin.setObjectName("rdpLogin")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.rdpLogin)
        self.label_4 = QtWidgets.QLabel(self.layoutWidget)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.rdpPassword = QtWidgets.QLineEdit(self.layoutWidget)
        self.rdpPassword.setObjectName("rdpPassword")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.rdpPassword)
        self.label_5 = QtWidgets.QLabel(self.layoutWidget)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.comboBox = QtWidgets.QComboBox(self.layoutWidget)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.comboBox)
        self.notifyAtDown = QtWidgets.QCheckBox(self.layoutWidget)
        self.notifyAtDown.setObjectName("notifyAtDown")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.notifyAtDown)
        self.notifyAtUp = QtWidgets.QCheckBox(self.layoutWidget)
        self.notifyAtUp.setObjectName("notifyAtUp")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.notifyAtUp)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Settings"))
        self.label.setText(_translate("Dialog", "IP Address"))
        self.ipAddress.setText(_translate("Dialog", "192.168.0.1"))
        self.label_2.setText(_translate("Dialog", "Name"))
        self.label_3.setText(_translate("Dialog", "RDP Login"))
        self.rdpLogin.setText(_translate("Dialog", "user"))
        self.label_4.setText(_translate("Dialog", "RDP Password"))
        self.label_5.setText(_translate("Dialog", "Connection"))
        self.comboBox.setItemText(0, _translate("Dialog", "Global Settings"))
        self.comboBox.setItemText(1, _translate("Dialog", "Remote Desktop"))
        self.comboBox.setItemText(2, _translate("Dialog", "RAdmin"))
        self.comboBox.setItemText(3, _translate("Dialog", "Web Browser"))
        self.notifyAtDown.setText(_translate("Dialog", "Notify at down host"))
        self.notifyAtUp.setText(_translate("Dialog", "Notify at up"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

