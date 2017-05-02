from PyQt5 import QtWidgets
from ui.mainWindow import MainWindow
import sys

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec_())
