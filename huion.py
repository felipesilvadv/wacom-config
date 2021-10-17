from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QKeySequenceEdit
from PyQt5.QtCore import QProcess
from PyQt5.uic import loadUi

class HuionTablet(QWidget):

    msg = QtCore.pyqtSignal(str)

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        loadUi('gui/wacom_widget.ui', self)
        # Agregar los procesos de cada boton
        # Quizás sea bueno dar la versatilidad de crear procesos 
        # a partir de la información rescatada con xsetwacom
        # todos los parametros de cada dispositivo.
        self.pushButton.clicked.connect(self.submit)
        self.processes = []
        self.processCount = 0


    def submit(self):
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
            "Button", str(num), f"key {value.lower()}"
        ])
        process.readyReadStandardError.connect(self.sendError)
        process.start()

    
    def setUpKey(self):
        self.processCount += 1
        if self.processCount == len(self.processes):
            self.parent.close()

    def sendError(self):
        process = self.sender()
        error = bytes(process.readAllStandardError()).decode()
        self.sendMessage(f'Hubo un error: {error}')

    def sendMessage(self, msg):
        self.msg.emit(msg)

    def closeEvent(self, event):
        if self.processCount < len(self.processes):
            self.sendMessage('Faltan procesos por terminar')
            return event.ignore()
        else:
            return event.accept()
