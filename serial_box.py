from PyQt5.QtWidgets import QComboBox
from PyQt5 import QtCore


class QSerialComboBox(QComboBox):
    pop_up = QtCore.pyqtSignal()
    def showPopup(self):
        self.pop_up.emit()
        super(QSerialComboBox, self).showPopup()
