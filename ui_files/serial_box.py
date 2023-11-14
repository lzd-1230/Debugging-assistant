from PyQt5.QtWidgets import QComboBox
from PyQt5 import QtCore


class QSerialComBox(QComboBox):
    pop_up = QtCore.pyqtSignal()
    def showPopup(self):
        self.pop_up.emit()
        super(QSerialComBox, self).showPopup()
