from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QProcess
from PyQt5.uic import loadUi

class HuionTablet(QWidget):

    def __init__(self):
        super().__init__()
        loadUi('gui/wacom_widget.ui', self)
        # Agregar los procesos de cada boton
        # Quizás sea bueno dar la versatilidad de crear procesos 
        # a partir de la información rescatada con xsetwacom
        # todos los parametros de cada dispositivo.
        

