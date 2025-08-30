import sys
import threading
import pyqtgraph as pg
from PyQt6 import QtWidgets, QtCore
import serial
from collections import deque

# 全局变量
data_queue = deque(maxlen=100)  # 存储数据
is_running = True  # 控制线程运行

# 串口读取线程
def serial_read_thread(port, baudrate):
    global data_queue, is_running

    # 打开串口
    ser = serial.Serial(port, baudrate, timeout=1)
    print(f"串口已打开: {port}")

    while is_running:
        try:
            # 读取一行数据
            line = ser.readline().decode("utf-8").strip()
            if line:
                # 假设数据格式为 "data1,data2,data3"
                data = list(map(float, line.split(",")))
                data_queue.append(data)  # 将数据添加到队列
        except Exception as e:
            print(f"串口读取错误: {e}")
            break

    # 关闭串口
    ser.close()
    print("串口已关闭")

# 主窗口类
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        # 设置窗口标题和大小
        self.setWindowTitle("多通道实时数据曲线")
        self.resize(800, 600)

        # 创建绘图部件
        self.plot_widget = pg.PlotWidget()
        self.setCentralWidget(self.plot_widget)

        # 设置绘图区域
        self.plot_widget.setLabel("left", "数据值")
        self.plot_widget.setLabel("bottom", "时间")
        self.plot_widget.setYRange(0, 100)  # Y 轴范围（下限为 0，上限为 100）
        self.plot_widget.showGrid(x=True, y=True)

        # 初始化曲线
        self.lines = []
        colors = ["r", "g", "b", "y", "m", "c"]  # 曲线颜色
        for i in range(3):  # 假设有 3 个数据通道
            pen = pg.mkPen(color=colors[i % len(colors)], width=2)
            line = self.plot_widget.plot(pen=pen, name=f"通道 {i+1}")
            self.lines.append(line)

        # 添加十字光标和标签
        self.crosshair_vline = pg.InfiniteLine(angle=90, movable=False)
        self.crosshair_hline = pg.InfiniteLine(angle=0, movable=False)
        self.plot_widget.addItem(self.crosshair_vline)
        self.plot_widget.addItem(self.crosshair_hline)

        self.label = pg.TextItem(anchor=(1, 1))
        self.plot_widget.addItem(self.label)

        # 绑定鼠标移动事件
        self.plot_widget.scene().sigMouseMoved.connect(self.on_mouse_moved)

        # 启动定时器
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(50)  # 每 50ms 更新一次

    def update_plot(self):
        global data_queue

        if not data_queue:
            return

        # 获取最新数据
        data = list(data_queue)[-1]  # 获取队列中最新的一条数据

        # 更新曲线
        for i, line in enumerate(self.lines):
            y_data = [d[i] for d in data_queue]  # 获取每个通道的数据
            line.setData(y_data)

        # 动态调整 Y 轴上限
        max_value = max([max([d[i] for d in data_queue]) for i in range(len(self.lines))])
        self.plot_widget.setYRange(0, max(100, max_value))  # Y 轴下限为 0，上限动态调整

    def on_mouse_moved(self, pos):
        # 获取鼠标位置对应的坐标
        mouse_point = self.plot_widget.plotItem.vb.mapSceneToView(pos)
        x = mouse_point.x()
        y = mouse_point.y()

        # 更新十字光标位置
        self.crosshair_vline.setPos(x)
        self.crosshair_hline.setPos(y)

        # 查找最近的曲线点
        text = ""
        for i, line in enumerate(self.lines):
            y_data = [d[i] for d in data_queue]
            if y_data:
                # 找到最接近鼠标位置的点的索引
                index = min(range(len(y_data)), key=lambda j: abs(j - x))
                value = y_data[index]
                text += f"通道 {i+1}: {value:.2f}\n"

        # 更新标签内容
        self.label.setText(text)
        self.label.setPos(x, y)

# 主程序
if __name__ == "__main__":
    # 串口配置
    port = "COM6"  # 修改为你的串口号
    baudrate = 115200

    # 启动串口读取线程
    thread = threading.Thread(target=serial_read_thread, args=(port, baudrate))
    thread.daemon = True  # 设置为守护线程
    thread.start()

    # 创建应用程序
    app = QtWidgets.QApplication(sys.argv)

    # 创建主窗口
    window = MainWindow()
    window.show()

    # 运行应用程序
    sys.exit(app.exec())

    # 关闭线程
    is_running = False
    thread.join()