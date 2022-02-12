import sys
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
        self.setWindowOpacity(0.9) # 窗口透明度
        self.cur_mode = 0      # 状态未连接
        self.widgets_init()
        self.vars_init()
        self.pic = Line_plot(self.ui.socket_graph)
    
    # 公共变量初始化
    def vars_init(self):
        self.cur_socket_mode = self.ui.socket_mode.currentText()
        self.cur_ip_choose = self.ui.ip_com.currentText()
        self.cur_port = self.ui.port_input.text()
        self.cur_recv_data_list = []
        self.data_dict = {
            "series1":[],
            "series2":[],
            "series3":[],
        }

    # 所有控件的初始化函数
    def widgets_init(self):
        self._com_box_init()
        self._btn_init()
        self._text_edit_init()
    
    def _text_edit_init(self):
        self.ui.port_input.textChanged.connect(self._get_addr)
        self.ui.port_input.setText("8080")
        
    # 拿到最新输入的端口号
    def _get_addr(self):
        self.cur_ip_choose = self.ui.ip_com.currentText()
        self.cur_port = self.ui.port_input.text()
        if(self.cur_port):
            self.ui.socket_switch.setEnabled(True)

    def _btn_init(self):
        # 默认开关不开
        self.ui.socket_switch.setEnabled(False)
        # 待完成
        # self.ui.socket_paint_switch.toggled.connect(self.paint_switch_handler)
        # self.save_socket_data.toggled.connect(save_data)
        self.ui.clear_data_btn.toggled.connect(self._clear_data)

    def _com_box_init(self):
        # 初始化当前的Ip列表
        ip_list = get_iplist()
        # 初始化下拉框内容
        self.ui.ip_com.addItems(ip_list)
        self.ui.ip_com.setCurrentText("0.0.0.0")
        self.ui.socket_mode.addItems(mode_list)
        # 初始化槽函数
        self.ui.ip_com.currentIndexChanged.connect(self._get_addr)
    
    def _clear_data(self):
        self.cur_recv_data_lits = []

    # 负责将接收到的数据存储在对象属性中
    def recv_data(self,cur_data):
        cur_data = cur_data.split(" ")
        # 限制内存中储存的数据量
        if(len(self.cur_recv_data_list) < 2000):
            # self.cur_recv_data_list.append(int(float(cur_data)))
            self.cur_recv_data_list.append(cur_data)
        for idx,key in enumerate(self.data_dict):
            self.data_dict[key].append(float(cur_data[idx]))

        # 给绘图类更新数据
        self.pic.new_data = True
        self.pic.data_dict = self.data_dict
        # 像文本框中写入内容
        self.ui.socket_recv_show.append(str(cur_data))
        # 绘图(想放在主函数中开启这个线程)
        # self.pic.plot(self.data_dict)




        


