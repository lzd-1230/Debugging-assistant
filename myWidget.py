import os
import time
import pandas as pd
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QApplication,QMainWindow
from PyQt5.QtGui import QIcon,QFont
from ui_Widget import Ui_MainWindow
from utils.com_utils import *
import utils.global_var as g
from Plot import Line_plot

class WidgetLogic(QMainWindow):
    def __init__(self,parent=None): # 单继承ui界面
        super().__init__()
        self.ui = Ui_MainWindow()     # self.ui就可以获得ui的属性
        self.ui.setupUi(self)  # 初始化UI界面
        # self.setWindowOpacity(0.9) # 窗口透明度
        self.cur_mode = 0      # 状态未连接
        self.widgets_init()
        self.pic = Line_plot(self.ui.socket_graph)
        self.pic_uart = Line_plot(self.ui.serial_graph)
        self.vars_init()
    
    # 公共变量初始化
    def vars_init(self):
        self.recv_data_on = True
        self.cur_socket_mode = self.ui.socket_mode.currentText()
        self.cur_ip_choose = self.ui.ip_com.currentText()
        self.cur_port = self.ui.port_input.text()
        self.uart_paint_recv = False

    # 所有控件的初始化函数
    def widgets_init(self):
        self._com_box_init()
        self._btn_init()
        self._text_edit_init()
    
    def _text_edit_init(self):
        self.ui.port_input.setText("8080")        
        self.ui.socket_switch.setEnabled(True)
        
    def _btn_init(self):
        # 默认开关不开
        self.ui.socket_switch.setEnabled(False)
        # 待完成
        self.ui.save_socket_data.clicked.connect(self.save_socket_recv_data)
        self.ui.save_uart_data_btn.clicked.connect(self.save_uart_recv_data)
        self.ui.clear_socket_data.clicked.connect(self._clear_socket_data)
        self.ui.clear_uart_data.clicked.connect(self._clear_uart_data)


    def _com_box_init(self):
        # 区分是socket还是uart的初始化!
        if(self.ui.tabWidget.currentWidget == "socket_tab"):
            ip_list = get_iplist()
            # 初始化下拉框内容
            self.ui.ip_com.addItems(ip_list)
            self.ui.ip_com.setCurrentText(ip_list[0])
            self.ui.socket_mode.addItems(mode_list)
        else:
            com_list = get_coms()
            self.ui.uart_com.addItems(com_list)
            baud_list = get_bauds()
            self.ui.baud_boxcom.addItems(baud_list)
            self.ui.baud_boxcom.setCurrentText("115200")
            g.set_var("baudrate","115200")
    
    def _clear_socket_data(self): 
        self.pic.data_dict = {key:[] for key in self.pic.pic_dict}
        # 绘图区数据清空
        for idx,key in enumerate(self.pic.data_dict):
            self.pic.pic_dict[key].clear()
        self.pic.p2_1.setData([])
        self.ui.socket_recv_show.clear()
        self.pic.cur_x = 0
        print("清除数据")

    def _clear_uart_data(self):
        self.pic_uart.data_dict = {key:[] for key in self.pic_uart.pic_dict}
        # 绘图区数据清空
        for idx,key in enumerate(self.pic_uart.data_dict):
            self.pic_uart.pic_dict[key].clear()
        self.pic_uart.p2_1.setData([])
        self.ui.uart_recv_show.clear()
        self.pic_uart.cur_x = 0
        print("清除数据")

    # 接收数据开关槽函数
    def recv_content_handle(self):
        if(self.ui.recv_data_btn.isChecked() == True):
            self.recv_data_on = True
        else:
            self.recv_data_on = False
            print("停止接收数据")
        
    # 负责将接收到的数据存储在对象属性中
    def socket_recv_data(self,cur_data):
        if self.recv_data_on:
            cur_data = cur_data.split(" ")
            if(self.pic.cur_x<10000):
                # 将每一列数据提取到字典中
                for idx,key in enumerate(self.pic.pic_dict):
                    self.pic.data_dict[key].append(float(cur_data[idx]))
                self.pic.cur_x += 1
            # 数据轮转
            else:
                pass
            # 给绘图类更新数据
            self.pic.new_data = True
            # 像文本框中写入内容
            self.ui.socket_recv_show.append(str(cur_data))

    # 串口接收数据的回调函数
    def uart_recv_data(self,cur_data:bytes):
        cur_data = cur_data.decode(encoding="utf8",errors="ignore")
        cur_data = cur_data.split(" ")
        if(self.uart_paint_recv):
            for idx,key in enumerate(self.pic_uart.pic_dict): 
                self.pic_uart.data_dict[key].append(float(cur_data[idx]))  # 画图数据
                # 在这里添加一个全局变量

            self.pic_uart.cur_x += 1
            self.pic_uart.new_data = True

        # 将数据赋值到写的窗口
        self.ui.uart_recv_show.append(str(cur_data))
        # 如果数据收发对话框打开了,则将数据写入


    # 保存socket接收的数据
    def save_socket_recv_data(self):
        data = pd.DataFrame(self.pic.data_dict)
        time_prefix = time.strftime("%Y-%m-%d-%H-%M-%S")
        with open("./data_save/"+time_prefix+"_socket"+".csv",mode="w",newline="") as f:
            data.to_csv(f)

        self.ui.socket_recv_show.append("数据保存成功")
        print("保存数据成功")
    
    # path
    def save_uart_recv_data(self):
        data = pd.DataFrame(self.pic_uart.data_dict)
        time_prefix = time.strftime("%Y-%m-%d-%H-%M-%S")
        if not os.path.isdir("./data_save"):
            os.mkdir("./data_save")
        with open("./data_save/"+time_prefix+"_uart"+".csv",mode="w",newline="") as f:
            data.to_csv(f)
        self.ui.socket_recv_show.append("数据保存成功")
        print("保存数据成功")





        


