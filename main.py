from PyQt5.QtWidgets import  QApplication, QMainWindow
from PyQt5.QtCore import QProcess
from PyQt5.uic import loadUi
from huion import HuionTablet
import sys

class AppWidget(QMainWindow):
    
    def __init__(self):
        super().__init__()
        loadUi('gui/main.ui', self)
        self.check_devices = QProcess(self)
        self.check_devices.setProgram('xsetwacom')
        self.check_devices.setArguments(['--list', 'devices'])
        self.check_devices.start()
        #self.check_devices.readyReadStandardOutput.connect(self.getOuput)
        self.check_devices.finished.connect(self.check_wacom)
        self.tablet = HuionTablet()
        self.setCentralWidget(self.tablet)
        self.centralWidget().setDisabled(True)
        self.show()

    
    def check_wacom(self):
        output = self.check_devices.readAllStandardOutput()
        if len(output):
            self.centralWidget().setEnabled(True)
        else:
            self.statusBar().showMessage('No se encontró una tableta Wacom')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    wid = AppWidget()
    sys.exit(app.exec())

