from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QTableWidget, QTableWidgetItem
from qfluentwidgets import  ProgressRing,TableWidget
from UI.Presetting import Ui_MainWindow

class Presetting(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setObjectName('b')
        self.tableWidget.setBorderVisible(True)
        self.tableWidget.setBorderRadius(8)

        self.tableWidget.setWordWrap(False)
        self.tableWidget.setRowCount(3)
        self.tableWidget.setColumnCount(5)

        songInfos = [
            ['预设1', '电压', '2V', '电流', '3A'],
            ['预设2', '电压', '3V', '电流', '3A'],
            ['预设3', '电压', '14V', '电流', '2A'],
        ]
        for i, songInfo in enumerate(songInfos):
            for j in range(5):
                self.tableWidget.setItem(i, j, QTableWidgetItem(songInfo[j]))

        # 设置水平表头并隐藏垂直表头
        self.tableWidget.setHorizontalHeaderLabels(['预设组', '电压', '电流', 'Year', 'Duration'])
        self.tableWidget.verticalHeader().hide()

