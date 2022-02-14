import sys
from myWidget import WidgetLogic
from Network import NetworkLogic
from PyQt5.QtWidgets import QApplication,QMainWindow
from PyQt5.QtGui import QIcon,QFont
import utils.global_var as g
from Network.stopThreading import stop_thread

class MainWindow(WidgetLogic,NetworkLogic,):
    def __init__(self, parent=None):
        super().__init__(parent)
        # 信号量初始化
        self.recv_content_signal.connect(self.recv_data)
        self.ui.socket_switch.toggled.connect(self.socket_control_handler)
        self.ui.recv_data_btn.toggled.connect(self.recv_content_handle)
        self.ui.socket_paint_switch.toggled.connect(self.paint_switch_handler)
        
    # 接收数据槽函数
    def recv_content_handle(self):
        if(self.ui.recv_data_btn.isChecked() == True):
            self.recv_data_on = True
            print("开始接收数据")
        else:
            self.recv_data_on = False
            print("停止接收数据")
    
    # 画图开关槽函数
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
                print("进入tcpserver模式")
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
    # 全局退出
    def closeEvent(self, event) -> None:
        """
        重写closeEvent方法，实现MainWindow窗体关闭时执行一些代码
        :param event: close()触发的事件
        """
        self.pic.stop()
        if(self.cur_mode == 1):
            self.close_conect()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    icon = QIcon(":/icons/image/关闭小.png")
    app.setWindowIcon(icon)
    font = QFont("Microsoft YaHei")
    app.setFont(font)
    # 设置qss样式
    with open("./style.qss") as f:
        qss = f.read()       
        app.setStyleSheet(qss)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_()) 