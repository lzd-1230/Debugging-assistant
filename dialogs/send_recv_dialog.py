import pandas as pd
import time
import asyncio
from  typing import Optional
from  ui_RecvSendArea import Ui_Dialog
from PyQt5.QtWidgets import QDialog,QFileDialog
from aioserial import AioSerial
from utils.read_file import get_data_from_file


class Data_Interact_dialog(QDialog):
    def __init__(self,save_btn_handler,serial_obj: Optional[AioSerial]=None):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle("数据收发区")
        self.save_btn_handler = save_btn_handler
        self.serial = serial_obj
        self.set_init_val()

    # 初始化
    def set_init_val(self):
        # 选项框初始化
        self.ui.text_recv_mode.click()
        self.ui.text_send_mode.click()

        # 槽函数初始化
        self.ui.clear_recv_area_btn.clicked.connect(self.clear_recv_area_handler)
        self.ui.clear_send_btn.clicked.connect(self.clear_send_area_handler)
        self.ui.save_data_btn.clicked.connect(self.save_btn_handler)
        self.ui.send_btn.clicked.connect(self.data_send_handler)
        self.ui.send_file_btn.clicked.connect(self.file_open)

    
    def file_open(self):
        file_dialog = QFileDialog(self,"读取数据文件","./") 
        file_path = file_dialog.getOpenFileName()[0]
        data_series = get_data_from_file(file_path)
        self.serial.loop.create_task(self.send_file_data(data_series))

    # 这个函数也要改成异步的
    async def send_file_data(self,data_series,step=5):
        for i in range(0,len(data_series),step):
            data_send = data_series[i:i+step]
            data_send = list(map(str,data_send))
            data_send = bytearray(" ".join(data_send).encode("ascii"))
            data_send.append(0x0d)
            data_send.append(0x0a)
            await self.serial.write_async(data_send)
            # print(f"send:{data_send}")
            await asyncio.sleep(0.1)
            

    # 发送输入框输入的内容
    def data_send_handler(self):
        data_input = self.ui.send_area.toPlainText()

        # 字符串发送
        if(self.ui.text_send_mode.isChecked()):
            if(self.serial is not None):
                bytesarr = bytearray(data_input.encode("ascii"))
                # "\n"强行换成"\r\n"
                if(bytesarr.endswith(b"\n")):
                    bytesarr[-1] = 0x0d
                    bytesarr.append(0x0a)
                else:
                    bytesarr.append(0x0d)
                    bytesarr.append(0x0a)

                _ = self.serial.write(bytesarr)

        # hex发送
        elif(self.ui.hex_send_mode.isChecked()):
            if(self.serial is not None):
                try:
                    data_list = data_input.split(" ")
                    data_list_hex = [int(ele,16) for ele in data_list]
                    self.serial.write(bytearray(data_list_hex))
                except Exception as e:
                    print(e)


    def clear_send_area_handler(self):
        self.ui.send_area.clear()

    def clear_recv_area_handler(self):
        self.ui.recv_area.clear()
    
    def save_recv_area_data(self):
        data = pd.DataFrame(self.pic_uart.data_dict)  # 数据字典如何获得??
        time_prefix = time.strftime("%Y-%m-%d-%H-%M-%S")
        with open("./data_save/"+time_prefix+"_uart"+".csv",mode="w",newline="") as f:
            data.to_csv(f)
        self.ui.socket_recv_show.append("数据保存成功")
        print("保存数据成功")
        
    
    # 析构
    def close_return(self):
        pass

