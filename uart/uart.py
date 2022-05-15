import sys
import os
sys.path.append(os.path.abspath("./"))  # 调试的时候当前目录找不到 utils
import utils.global_var as g
import asyncio
import aioserial
import struct
from quamash import QEventLoop
from PyQt5.QtCore import pyqtSignal

class Uart():
    uart_recv_content_signal = pyqtSignal(bytes) # 收到数据的信号

    def __init__(self):
        pass

    def get_uart_info(self):
        self.port = g.get_var("uart_port")
        self.baudrate = g.get_var("baudrate")

    # 开启串口
    def com_init(self):
        self.get_uart_info()
        self.loop = QEventLoop()
        asyncio.set_event_loop(self.loop) 
        self.serial = aioserial.AioSerial(port=self.port, baudrate=self.baudrate,loop=self.loop ,parity='N', stopbits=1, timeout=None, xonxoff=False, rtscts=False) 
        
        print("串口打开")
        print(f"current port:{self.port} cur baudrate:{self.baudrate}")
        self.loop.create_task(self.start_com()) # 往里面提交任务
            
    async def read_and_print(self,aioserial_instance: aioserial.AioSerial):
        while g.get_var("com_status"):
            data_len_b: bytes = await aioserial_instance.read_async(2)
            # print(f"原始:{data_len_b}")
            data_len = data_len_b.decode()
            # print(f"长度位:{data_len}")
            # 读掉后面的回车!
            _ = None
            while(_ != b'\n'):
                _ = await aioserial_instance.read_async()# win下的换行是\r\n两个字节

            data =  await aioserial_instance.read_async(int(data_len))
            print(f"数据:{data}")
    
            _ = ""

            # print(f"second round :{_}")
            while(_ != b'\n'):
                _ = await aioserial_instance.read_async()
            
            print(f"second round:{_}")
            if(data):
                self.uart_recv_content_signal.emit(data)

    async def start_com(self):
        coro = self.read_and_print(self.serial)
        com_task = self.loop.create_task(coro) 

if __name__ == "__main__":
    u = Uart()
    print(u.uart_com_list)
