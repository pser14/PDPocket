from time import sleep
import PyQt6
import serial
import serial.tools.list_ports
import time



class SerialDevice:
    def __init__(self, com):
        self.read_voltage = "MEAS:VOLT?"
        self.read_current = "MEAS:CURR?"
        self.read_power = "MEAS:POW?"
        self.read_version = "SYST:VERS?"
        self.read_temperature = "gettemp 1"
        self.get_data =  "getmsg 1"
        self.ser = self.initialize_serial(com)

    def initialize_serial(self, com):
        ser = serial.Serial(
            port=com,
            baudrate=115200,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
        )
        return ser

    def find_port(self):
        ports = serial.tools.list_ports.comports()
        if not ports:
            PortFlag = "未找到任何串口设备"
            print("No ports found")
            return PortFlag

        port_list = []
        for port in ports:
            port_info = port.device
            port_list.append(port_info)
            print(port_list)
        return port_list

    def once_read(self, message):
        try:
            self.ser.write(message.encode('ascii'))
            print(f"[test]发送: {message}")
            time.sleep(0.1)
            if self.ser.in_waiting:
                data = self.ser.readline()
                return data.decode('utf-8').rstrip()
            else:
                return None
        except serial.SerialException as e:
            print(f"串行通信错误: {e}")
        except Exception as e:
            print(f"发生错误: {e}")

    def voltage_set(self, vol_value):
        output_voltage = f"VOLT {vol_value}"
        try:
            self.ser.write(output_voltage.encode('ascii'))
            print(f"[test]发送: VOLT {vol_value}")
            time.sleep(0.1)
        except serial.SerialException as e:
            print(f"串行通信错误: {e}")
        except Exception as e:
            print(f"发生错误: {e}")

    def voltage_up(self, step):
        output_step = f"VOLT:STEP {step}"
        try:
            self.ser.write(output_step.encode('ascii'))
            print(f"[test]发送:  {output_step}")
            time.sleep(0.1)
            self.ser.write("VOLT UP".encode('ascii'))
            print(f"[test]发送: VOLT UP")
            time.sleep(0.1)
        except serial.SerialException as e:
            print(f"串行通信错误: {e}")
        except Exception as e:
            print(f"发生错误: {e}")

    def current_set(self, curr_value):
        output_current = f"CURR {curr_value}"
        try:
            self.ser.write(output_current.encode('ascii'))
            print(f"[test]发送: {output_current}")
            time.sleep(0.1)
        except serial.SerialException as e:
            print(f"串行通信错误: {e}")
        except Exception as e:
            print(f"发生错误: {e}")

    def current_up(self, step):
        output_step = f"CURR:STEP {step}"
        try:
            self.ser.write(output_step.encode('ascii'))
            print(f"[test]发送:  {output_step}")
            time.sleep(0.1)
            self.ser.write("CURR UP".encode('ascii'))
            print(f"[test]发送: CURR UP")
            time.sleep(0.1)
        except serial.SerialException as e:
            print(f"串行通信错误: {e}")
        except Exception as e:
            print(f"发生错误: {e}")

    def current_max_input(self, curr_value):
        input_current = f"setibat {curr_value}"
        try:
            self.ser.write(input_current.encode('ascii'))
            print(f"[test]发送: {input_current}")
            time.sleep(0.1)
        except serial.SerialException as e:
            print(f"串行通信错误: {e}")
        except Exception as e:
            print(f"发生错误: {e}")

    def power_max_output(self, power_value):
        power_max_output = f"setibat {power_value}"
        try:
            self.ser.write(power_max_output.encode('ascii'))
            print(f"[test]发送: {power_max_output}")
            time.sleep(0.1)
        except serial.SerialException as e:
            print(f"串行通信错误: {e}")
        except Exception as e:
            print(f"发生错误: {e}")

    def output_on(self):
        try:
            self.ser.write("OUTP ON".encode('ascii'))
            print(f"[test]发送: OUTP ON")
            time.sleep(0.1)
        except serial.SerialException as e:
            print(f"串行通信错误: {e}")
        except Exception as e:
            print(f"发生错误: {e}")

    def output_off(self):
        try:
            self.ser.write("OUTP OFF".encode('ascii'))
            print(f"[test]发送: OUTP OFF")
            time.sleep(0.1)
        except serial.SerialException as e:
            print(f"串行通信错误: {e}")
        except Exception as e:
            print(f"发生错误: {e}")

    def key_lock(self, lock):
        lock_status = f"lockkey {lock}"
        try:
            self.ser.write(lock_status.encode('ascii'))
            print(f"[test]发送: {lock_status}")
            time.sleep(0.1)
        except serial.SerialException as e:
            print(f"串行通信错误: {e}")
        except Exception as e:
            print(f"发生错误: {e}")

    def short_circuit_protection(self, protection):
        short_circuit_protection = f"setSFB {protection}"
        try:
            self.ser.write(short_circuit_protection.encode('ascii'))
            print(f"[test]发送: {short_circuit_protection}")
            time.sleep(0.1)
        except serial.SerialException as e:
            print(f"串行通信错误: {e}")
        except Exception as e:
            print(f"发生错误: {e}")

    def set_device_name(self, name):
        device_name = "setname " + name
        try:
            self.ser.write(device_name.encode('ascii'))
            print(f"[test]发送: {device_name}")
            time.sleep(0.1)
        except serial.SerialException as e:
            print(f"串行通信错误: {e}")
        except Exception as e:
            print(f"发生错误: {e}")

    def preset_start(self, preset):
        preset_start = f"startPreset {preset}"
        try:
            self.ser.write(preset_start.encode('ascii'))
            print(f"[test]发送: {preset_start}")
            time.sleep(0.1)
        except serial.SerialException as e:
            print(f"串行通信错误: {e}")
        except Exception as e:
            print(f"发生错误: {e}")

    def preset_set(self, preset, step, vol, curr, keep_time, loop):
        preset_set = f"preset {preset} {step} {vol} {curr} {keep_time}"
        try:
            self.ser.write(preset_set.encode('ascii'))
            print(f"[test]发送: {preset_set}")
            time.sleep(0.1)
            self.ser.write(f"preset {preset} 30 {loop}".encode('ascii'))
            time.sleep(0.1)
            self.ser.write(f"save preset {preset}".encode('ascii'))
        except serial.SerialException as e:
            print(f"串行通信错误: {e}")
        except Exception as e:
            print(f"发生错误: {e}")

    def subscribe_start(self, loop_time):
        subscribe_start = f"getmsg {1}"
        try:
            self.ser.write(subscribe_start.encode('ascii'))
            print(f"[test]发送: {subscribe_start}")
            time.sleep(0.1)
        except serial.SerialException as e:
            print(f"串行通信错误: {e}")
        except Exception as e:
            print(f"发生错误: {e}")

    def data_analysis(self, data):
        try:
            self.ser.write(data.encode('ascii'))
            print(f"[test]发送: {data}")
            time.sleep(0.1)
            if self.ser.in_waiting:
                data = self.ser.readline()
                data_hex = data.hex()
                for i in range(0, len(data_hex), 48):
                    group_24bit = data_hex[i:i + 48]
                    if len(group_24bit) == 48:
                        groups_4bit = [group_24bit[j:j + 8] for j in range(0, 48, 8)]
                        string_data = groups_4bit.decode('utf-8')
                        print(f"24位组: {group_24bit} -> 4位组: {string_data}")

                    else:
                        print(f"忽略不完整的数据组: {group_24bit}")
            else:
                return None
        except serial.SerialException as e:
            print(f"订阅数据错误：{e}")
        except Exception as e:
            print(f"订阅错误{e}")

    def close(self):
        self.ser.close()

if __name__ == '__main__':
    device = SerialDevice("COM6")


    while True:
        message = device.read_current
        print(device.once_read(message))
        sleep(0.01)





    # if device.ser.isOpen():
    #     print("串行端口已打开")
    # message = device.get_data
    # print(device.data_analysis(message))
    # while True:
    #     if device.ser.in_waiting:
    #         data = device.ser.readline()
    #         data_hex = data.hex()
    #         for i in range(0, len(data_hex), 48):
    #             group_24bit = data_hex[i:i + 48]
    #             if len(group_24bit) == 48:
    #                 groups_4bit = [group_24bit[j:j + 8] for j in range(0, 48, 8)]
    #                 groups_int = [int(group, 16) for group in groups_4bit]
    #                 print(groups_int)
    #                 print(f"24位组: {group_24bit} -> 4位组: {groups_4bit}")
    #             else:
    #                 print(f"忽略不完整的数据组: {group_24bit}")

    #     message = device.get_data
    #     print(device.data_analysis(message))
    #     # device.voltage_set(4)
    #     # time.sleep(2)
    #     # device.voltage_up(0.5)
    #     # time.sleep(2)
    #     # device.current_set(0.5)
    #     # time.sleep(2)
    #     # device.current_up(0.5)
    #     # time.sleep(2)
    #     # message = device.read_voltage
    #     # print(device.once_read(message))
    #     # message = device.read_current
    #     # print(device.once_read(message))
    #     # device.output_on()
    #     # time.sleep(2)
    #     device.output_off()
    #     if message == "exit":
    #         break
    #     time.sleep(1)
    # device.close()
