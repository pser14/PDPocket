import serial.tools.list_ports


def get_serial_ports():
    """
    获取所有串口设备并存储为数组
    :return: 包含所有串口设备信息的列表
    """
    # 获取所有串口设备
    ports = serial.tools.list_ports.comports()

    # 将设备信息存储为字典列表
    port_list = []
    for port in ports:
        port_info = {port.device}
        port_list.append(port_info)
        print(port_list[0])

    return port_list


if __name__ == "__main__":
    # 获取所有串口设备
    serial_ports = get_serial_ports()

