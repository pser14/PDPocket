from qfluentwidgets import NavigationItemPosition,FluentWindow
from qfluentwidgets import  FluentIcon as FIF
from SettingWindow import SettingWindow
from HighSetting import HighSetting
from Prsetting import Presetting
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QApplication,QWidget

class MainWindow(FluentWindow,QtWidgets.QWidget):
    def __init__(self):
        super(MainWindow,self).__init__()
        self.resize(1000, 580)
        self.setWindowTitle("PDPocket")
        self.HighSetting = HighSetting()
        self.Presetting = Presetting()
        self.settingWindow = SettingWindow()

        self.addSubInterface(self.settingWindow,FIF.EDIT,'基础信息',NavigationItemPosition.TOP)
        self.addSubInterface(self.HighSetting,FIF.SETTING,'高级设置',NavigationItemPosition.SCROLL)
        self.addSubInterface(self.Presetting,FIF.ADD,'预设重置',NavigationItemPosition.SCROLL)



app = QApplication([])
window = MainWindow()
window.show()
app.exec()
