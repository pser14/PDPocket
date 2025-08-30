import sys
from PyQt6.QtWidgets import QMainWindow,QApplication,QWidget
from qfluentwidgets import  ProgressRing
from UI.HighSetting import Ui_MainWindow

class HighSetting(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)