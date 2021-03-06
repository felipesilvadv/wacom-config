from PyQt5.QtWidgets import  QApplication, QMainWindow
from PyQt5.QtCore import QProcess
from PyQt5.uic import loadUi
from huion import HuionTablet, Stylus
import sys

class AppWidget(QMainWindow):
    
    def __init__(self):
        super().__init__()
        loadUi('gui/main.ui', self)
        self.check_devices = QProcess(self)
        self.check_devices.setProgram('xsetwacom')
        self.check_devices.setArguments(['--list', 'devices'])
        self.check_devices.start()
        self.check_devices.finished.connect(self.check_wacom)
        self.tablet = HuionTablet(self.tabWidget)
        self.stylus = Stylus(self.tabWidget)
        self.tablet.msg.connect(self.statusBar().showMessage)
        self.tablet.finish.connect(self.close)
        self.tabWidget.addTab(self.tablet, 'Tablet')
        self.tabWidget.addTab(self.stylus, 'Stylus')
        self.show()
        #self.setCentralWidget(self.tablet)
        #self.centralWidget().setDisabled(True)
        #self.show()

    
    def check_wacom(self):
        output = self.check_devices.readAllStandardOutput()
        if len(output):
            self.centralWidget().setEnabled(True)
        else:
            self.statusBar().showMessage('No se encontrĂ³ una tableta Wacom')

    def closeEvent(self, event):
        return self.tablet.closeEvent(event)
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    wid = AppWidget()
    sys.exit(app.exec())

