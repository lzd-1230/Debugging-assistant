import sys
from PyQt5.QtWidgets import QApplication,QMainWindow,QDialog
from PyQt5.QtGui import QIcon,QFont
from PyQt5.QtCore import pyqtSlot
from myWidget import WidgetLogic
from Network import NetworkLogic
from uart import UartLogic
import utils.global_var as g
from Network.stopThreading import stop_thread
from ui_ConfigDialog import Ui_Dialog
import time
import asyncio
from dialogs.uart_config_dialog import Uart_Config_dialog
from dialogs.send_recv_dialog import Data_Interact_dialog

class MainWindow(WidgetLogic,NetworkLogic,UartLogic):
    """主窗口类"""
    def __init__(self,app,loop,parent=None):
        super().__init__(parent)   # 这里是WidgetLogic的初始化函数
        self.app = app
        self.loop = loop
        # 不同类的方法属性绑定
        self.socket_recv_content_signal.connect(self.socket_recv_data)  # NetworkLogic类的类属性
        self.uart_recv_content_signal.connect(self.uart_recv_data)
        self.ui.uart_config_btn.clicked.connect(self.uart_dialog_raise)
        self.ui.data_show_dialog.clicked.connect(self.data_interact_dialog_raise)

        self.ui.socket_switch.toggled.connect(self.socket_control_handler) # WidgetLogic类的方法
        self.ui.com_switch.toggled.connect(self.com_control_handler)
        self.ui.recv_data_btn.toggled.connect(self.recv_content_handle) # designer中的属性
        self.ui.socket_paint_switch.toggled.connect(self.paint_switch_handler) # 自己的逻辑函数
        self.ui.uart_paint_switch.toggled.connect(self.uart_paint_switch_handler)
        self.ui.port_input.textChanged.connect(self._get_addr)
        self.ui.ip_com.currentTextChanged.connect(self._ip_com_change_handler)
        self.ui.uart_com.currentTextChanged.connect(self._uart_port_change_handler)
        self.ui.baud_boxcom.currentTextChanged.connect(self._baud_change_handler)

    # ip端口改变的槽函数
    @pyqtSlot(str)
    def _ip_com_change_handler(self,cur_text):
        g.set_var("listen_ip",cur_text)  # 公共变量设置
        self.get_addr()

    @pyqtSlot(str) 
    def _uart_port_change_handler(self,cur_text):
        g.set_var("uart_port",cur_text)
        self.get_uart_info()

    @pyqtSlot(str)
    def _baud_change_handler(self,cur_text):
        g.set_var("baudrate",int(cur_text))
        self.get_uart_info()

    # 串口参数修改对话框
    def uart_dialog_raise(self):
        uart_config_dialog = Uart_Config_dialog()
        # 初值获取
        curve_num = self.pic_uart.curve_num
        attention_range = self.pic_uart.attention_range

        uart_config_dialog.set_init_val(attention_range=attention_range,
                            curve_num=curve_num)

        res = uart_config_dialog.exec()  # 关闭后拿到是否修改

        if(res == QDialog.DialogCode.Accepted):
            ret = uart_config_dialog.close_return()
            # 完成数据的赋值
            self.pic_uart.attention_range = ret[0] 
            self.pic_uart.curve_num = ret[1]
            self.pic_uart.p1.clear()    # 清除所有
            self.pic_uart.reconfig_curve()  # 重新初始化绘图框(其实只用初始化一部分就可以了)

    def data_interact_dialog_raise(self):
        """数据交互窗口打开"""
        self.data_interact_dialog_isopened = True
        self.data_interact_dialog = Data_Interact_dialog(self.save_uart_recv_data) # WidgetLogic中也是可以拿到这个对象的!
        self.data_interact_dialog.exec()

        self.data_interact_dialog_isopened = False


    # 将最新的地址写入公共变量字典
    def _get_addr(self):
        try:
            g.set_var("listen_port",int(self.ui.port_input.text())) 
            print(f"prot:{int(self.ui.port_input.text())}")
        except TypeError:
            print("输入正确类型的端口号")
        # 只有拿到了端口号,才可以打开连接开关
        if(self.ui.port_input.text()):
            self.ui.socket_switch.setEnabled(True)
        self.get_addr()

    # socket画图开关槽函数(和com口的基本重复)
    def paint_switch_handler(self):
        if(self.ui.socket_paint_switch.isChecked() == True):
            if not self.pic.first_on:
                self.pic.first_on = True
                self.pic.start()
            else:
                self.pic.resume()
        else:
            self.pic.pause()
            
    # 控制socket的开关函数
    def socket_control_handler(self):
        # 开启连接
        if self.ui.socket_switch.isChecked() == True:
            # 首先判断当前模式
            if self.cur_socket_mode == "Tcp_Server":
                # 变量初始化
                self.cur_mode = 1
                g.set_var("socket_status",True)
                self.port = int(self.cur_port)
                self.listen_ip = self.cur_ip_choose

                self.server_init() # socket服务端监听线程
        # 关闭连接
        else:
            g.set_var("socket_status",False)
            # 关闭服务端监听和连接
            self.close_conect()
    
    # uart画图开关槽函数
    def uart_paint_switch_handler(self):
        if(self.ui.uart_paint_switch.isChecked() == True):
            self.uart_paint_recv = True
            # 判断是开启还是继续
            if(not self.pic_uart.first_on):
                self.pic_uart.first_on = True
                self.pic_uart.start()
            else:
                self.pic_uart.resume()
        else:
            self.uart_paint_recv = False
            self.ui.uart_com.setEnabled(True)
            self.ui.baud_boxcom.setEnabled(True)
            self.pic_uart.pause()

    # 控制串口开关的函数
    def com_control_handler(self):
        if self.ui.com_switch.isChecked() == True:
            self.ui.uart_com.setEnabled(False)
            self.ui.baud_boxcom.setEnabled(False)
            g.set_var("com_status",True)
            self.com_init(self.loop)
        else:
            self.ui.uart_com.setEnabled(True)
            self.ui.baud_boxcom.setEnabled(True)
            print("串口关闭!")
            g.set_var("com_status",False)
            self.serial.close()  # 暴力关闭,让协程结束!
            
    # 全局退出
    def closeEvent(self, event) -> None:
        """
        重写closeEvent方法，实现MainWindow窗体关闭时执行一些代码
        :param event: close()触发的事件
        """
        # 如果画图线程启动了之后,在主线程关闭后,子线程不需要手动关闭?
        
        print("全局退出函数")
        if(self.ui.uart_paint_switch.isChecked()):
            print("do pic_uart stop")
            # self.pic_uart.resume()
            self.pic_uart.stop()
        
        if(self.ui.socket_paint_switch.isChecked()):
            print("do pic stop")
            self.pic.stop()

        if(self.cur_mode == 1):
            self.close_conect()

        # 退出事件循环!
        # if(self.loop.is_running()):
       
        self.serial.close()  # 它会自动帮我们判断
        print("loop is running")
        self.loop.stop()
        self.loop.close() 
        print(f'loop is closed:{self.loop.is_closed()}')
        sys.exit()   # 直接让线程退出,这样事件循环就退出了???并没有...


if __name__ == "__main__":
    app = QApplication(sys.argv)
    from quamash import QEventLoop
    loop = QEventLoop(app)
    
    icon = QIcon(":/icons/image/关闭小.png")
    app.setWindowIcon(icon)
    font = QFont("Microsoft YaHei")
    app.setFont(font)

    # 设置qss样式
    with open("./style.qss") as f:
        qss = f.read()       
        app.setStyleSheet(qss)

    win = MainWindow(app,loop)
    win.show()
    print("run the loop")
    sys.exit(app.exec_())