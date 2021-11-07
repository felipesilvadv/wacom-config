from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QKeySequenceEdit, QGraphicsScene
from PyQt5.QtCore import QProcess
from PyQt5.uic import loadUi

class HuionTablet(QWidget):

    msg = QtCore.pyqtSignal(str)
    finish = QtCore.pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        loadUi('gui/wacom_widget.ui', self)
        # Agregar los procesos de cada boton
        # Quizás sea bueno dar la versatilidad de crear procesos 
        # a partir de la información rescatada con xsetwacom
        # todos los parametros de cada dispositivo.
        self.pushButton.clicked.connect(self.submit)
        self.processes = []
        self.processCount = 0


    def submit(self):
        process = QProcess(self)
        process.setProgram('xsetwacom')
        process.setArguments([
            '--set', 'HUION Huion Tablet stylus',
            "Button", '2', f"key shift"
        ])
        process.start()
        for key in filter(lambda x: isinstance(getattr(self, x), QKeySequenceEdit), self.__dict__):
            obj = getattr(self, key)
            value = obj.keySequence().toString()
            num = obj.objectName()[-1]
            self.createProcess(value, num)
        
        
    
    def createProcess(self, value, num):
        process = QProcess(self)
        self.processes.append(process)
        process.finished.connect(self.setUpKey)
        process.setProgram('xsetwacom')
        process.setArguments([
            '--set', 'HUION Huion Tablet Pad pad',
            "Button", str(num), f"key {value.lower().replace('+', ' + ')}"
        ])
        process.readyReadStandardError.connect(self.sendError)
        process.start()

    
    def setUpKey(self):
        self.processCount += 1
        if self.processCount == len(self.processes):
            self.finish.emit()

    def sendError(self):
        process = self.sender()
        error = bytes(process.readAllStandardError()).decode()
        self.error = True
        self.sendMessage(f'Hubo un error: {error}')

    def sendMessage(self, msg):
        self.msg.emit(msg)

    def closeEvent(self, event):
        if self.processCount < len(self.processes):
            self.sendMessage('Faltan procesos por terminar')
            return event.ignore()
        elif self.error:
            return event.ignore()
        else:
            return event.accept()


class Stylus(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        loadUi('gui/stylus.ui', self)
