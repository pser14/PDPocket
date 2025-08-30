import sys
import random
import numpy as np
import pyqtgraph as pg
from PyQt6.QtWidgets import QMainWindow,QApplication,QWidget
from PyQt6 import QtCore, QtGui, QtWidgets
from qfluentwidgets import  ProgressRing,SwitchButton,ComboBox
from queue import Queue
from UI.PDPocket import Ui_MainWindow
from PD_Pocket_API import SerialDevice as SD

class DataThread(QtCore.QThread):
    def __init__(self, data_queue):
        super().__init__()
        self.data_queue = data_queue
        self.running = True
        self.device = SD("com6")

    def run(self):
        while self.running:
            # new_value = random.uniform(-1, 1)
            message = "MEAS:VOLT?"
            new_value = []
            new_value.append(self.device.once_read("MEAS:CURR?"))
            new_value.append(self.device.once_read("MEAS:VOLT?"))
            # print(new_value_volt, new_value_curr)
            self.data_queue.put(new_value)
            self.msleep(30)

    def stop(self):
        self.running = False
        self.wait()

class SettingWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setObjectName('a')
        self.progressBar_5.setTextVisible(True)
        self.progressBar_5.setRange(0, 100)
        self.progressBar_5.setValue(26)
        self.progressBar_5.setFormat("%v℃")
        self.progressBar_6.setTextVisible(True)
        self.progressBar_6.setRange(0, 100)
        self.progressBar_6.setValue(6)
        self.progressBar_6.setFormat("%vA")
        self.progressBar_7.setTextVisible(True)
        self.progressBar_7.setRange(0, 100)
        self.progressBar_7.setValue(20)
        self.progressBar_7.setFormat("%vV")

        self.plot_widget = pg.PlotWidget(self)
        self.plot_widget.setGeometry(QtCore.QRect(140, 0, 620, 320))
        # self.plot_widget.setBackground(background= )

        self.curve = self.plot_widget.plot(pen='y') #对曲线进行初始化
        self.data = np.zeros(200)
        self.plot_widget.setLabel('left', '数值')
        self.plot_widget.setLabel('bottom', '时间')
        self.plot_widget.setYRange(0, 1.5)
        self.plot_widget.showGrid(True, True)

        self.data_queue = Queue()
        self.adjust_y_axis()

        # 启动工作线程
        self.data_thread = DataThread(self.data_queue)
        self.data_thread.start()
        # 定时器更新数据
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(20)

        # self.select_port()
        # self.BaudRate()


    def update_data(self):
        while not self.data_queue.empty():
            new_value = self.data_queue.get()
            print(new_value[1])
            if new_value[0] != None:
                self.textBrowser_voltage.setText(str(new_value[1]))
                self.textBrowser_current.setText(str(new_value[0]))
                self.progressBar_7.setValue(int(float(new_value[0])))
                self.data = np.roll(self.data, -1)
                self.data[-1] = new_value[0]
                self.curve.setData(self.data)
                self.adjust_y_axis()
                self.plot_widget.setXRange(len(self.data) - 50, len(self.data))

    def adjust_y_axis(self):
        """根据数据动态调整 Y 轴范围"""
        if len(self.data) > 0:
            recent_data = self.data[-15:]
            print(recent_data)
            min_value = np.min(self.data)
            max_value = max(recent_data)

            # 添加缓冲区域（10% 的额外空间）
            buffer = (max_value - min_value) * 0.5
            y_max = max_value + buffer

            # 设置 Y 轴范围
            self.plot_widget.setYRange(0,y_max)


    def closeEvent(self, event):
        self.data_thread.stop()
        event.accept()

    def callback_selectPort(self):
        current_device = self.comboBox_selectPort.currentText()
        print(self.comboBox_selectPort.currentText())
        return current_device

    def callback_BaudRate(self):
        current_BaudRate = self.comboBox_setBaud.currentText()
        return current_BaudRate

    def select_port(self):
        self.device = SD.find_port(self)
        if self.device == "未找到任何串口设备":
            self.comboBox_selectPort.setPlaceholderText("请插入设备")
        else:
            self.comboBox_selectPort.addItems(self.device)
        self.comboBox_selectPort.currentIndexChanged.connect(self.callback_selectPort)

    def BaudRate(self):
        BaudRate = ['115200','57600','38400','19200','9600']
        self.comboBox_setBaud.addItems(BaudRate)
        self.comboBox_setBaud.currentIndexChanged.connect(self.callback_BaudRate)

app = QApplication([])
window = SettingWindow()
window.show()
app.exec()