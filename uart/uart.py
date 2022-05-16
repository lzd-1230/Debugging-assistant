import sys
import os
sys.path.append(os.path.abspath("./"))  # 调试的时候当前目录找不到 utils
import utils.global_var as g
import asyncio
import aioserial
import struct
from quamash import QEventLoop
from PyQt5.QtCore import pyqtSignal
from serial.serialutil import PortNotOpenError

class Uart():
    uart_recv_content_signal = pyqtSignal(bytes) # 收到数据的信号

    def __init__(self):
        pass

    def get_uart_info(self):
        self.port = g.get_var("uart_port")
        self.baudrate = g.get_var("baudrate")

    # 开启串口
    def com_init(self,loop):
        self.get_uart_info()
        self.loop = loop
        print(f"创建串口任务之前事件循环已经开始{self.loop.is_running()}")
        asyncio.set_event_loop(self.loop) 
        self.serial = aioserial.AioSerial(port=self.port, baudrate=self.baudrate,loop=self.loop) 
        print(f"open current port:{self.port} cur baudrate:{self.baudrate}")
        self.listen_task = self.loop.create_task(self.start_com()) # 往里面提交任务

    async def read_and_print(self,aioserial_instance: aioserial.AioSerial):
        while True:
            if(not g.get_var("com_status")):
                print("enter close")
                aioserial_instance.close()
                break
            try:
                data_len_b: bytes = await aioserial_instance.read_async(2)
            except PortNotOpenError as e:
                break

            data_len = data_len_b.decode()
            # 读掉后面的回车!
            _ = None
            while(_ != b'\n'):
                try:
                    _ = await aioserial_instance.read_async()# win下的换行是\r\n两个字节
                except PortNotOpenError as e:
                    break
            try:
                print(data_len)
                data =  await aioserial_instance.read_async(int(data_len))
            except PortNotOpenError as e:
                break
            print(f"数据:{data}")
    
            _ = ""
            while(_ != b'\n'):
                try:
                    _ = await aioserial_instance.read_async()
                except PortNotOpenError as e:
                    break
            
            if(data):
                self.uart_recv_content_signal.emit(data)
      

    async def start_com(self):
        coro = self.read_and_print(self.serial)
        com_task = self.loop.create_task(coro) 

if __name__ == "__main__":
    u = Uart()
    print(u.uart_com_list)
