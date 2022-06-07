import pandas as pd
import time
from  ui_RecvSendArea import Ui_Dialog
from PyQt5.QtWidgets import QDialog

class Data_Interact_dialog(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle("数据收发区")
        self.set_init_val()
        
    # 初始化
    def set_init_val(self):
        # 选项框初始化
        self.ui.text_recv_mode.click()
        self.ui.text_send_mode.click()

        # 槽函数初始化
        self.ui.clear_recv_area_btn.clicked.connect(self.clear_recv_area_handler)
        self.ui.clear_send_btn.clicked.connect(self.clear_send_area_handler)
    
    def clear_send_area_handler(self):
        self.ui.send_area.clear()

    def clear_recv_area_handler(self):
        self.ui.recv_area.clear()
    
    def save_recv_area_data(self):
        data = pd.DataFrame(self.pic_uart.data_dict)  # 把数据字典
        time_prefix = time.strftime("%Y-%m-%d-%H-%M-%S")
        with open("./data_save/"+time_prefix+"_uart"+".csv",mode="w",newline="") as f:
            data.to_csv(f)
        self.ui.socket_recv_show.append("数据保存成功")
        print("保存数据成功")
        
    
    # 析构
    def close_return(self):
        pass
