import socket
import struct
import time
from Network.stopThreading import stop_thread
import threading
from PyQt5.QtCore import pyqtSignal,QObject
"""
tcp服务端的基本实现框架
"""
class MyTcpServer():
    # 接收到数据的信号
    recv_content_signal = pyqtSignal(str)
    def __init__(self) -> None:
        # ip和端口要自动获取,不能指定成参数
        self.clients_list = []
        # self.server_init()  # 要在main的类中启动
        self.listen_ip = "0.0.0.0"
        self.port = 8080
    # 初始化
    def server_init(self):
        self.server =  socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.setblocking(False)  # 设置非阻塞模式
        self.server.bind((self.listen_ip,self.port))
        self.server.listen(5)
        self.start_listen_thread()
        print(f"已监听了{self.listen_ip}:{self.port}")
        print("----waiting for connect----")

    # 启动线程函数(!!!这个函数一定要在main.py中去调用,因为那个类才继承了QObject)
    def start_listen_thread(self):
        # return self.server.accept() # 建成一个链接(主进程)
        self.listen_thread = threading.Thread(target=self.handle)
        self.listen_thread.start()

    # 处理客户端数据
    def handle(self):
        while True:
            try:
                client_socket,client_addr = self.server.accept()
            except Exception:
                time.sleep(0.02)
            else:
                self.clients_list.append((client_socket,client_addr))
                print(f"{client_addr}已经建立连接")
            # 遍历客户端列表来接收数据
            for client_socket,client_addr in self.clients_list:
                try:
                    data_len = client_socket.recv(4)
                    data_len = struct.unpack("I", data_len)[0]
                    recv_data = client_socket.recv(data_len)
                except Exception as e:
                    pass
                
                # 如果接收到了数据才发送
                else:
                    if recv_data:
                        data = recv_data.decode("utf-8")
                        self.recv_content_signal.emit(data) # 数据以元组形式传递
    # 关闭监听和所有连接
    def close_conect(self):

        for client,addr in self.clients_list:
            client.shutdown(socket.SHUT_RDWR) # 关闭连接，并且不允许继续发送和接收
            client.close()
        self.clients_list = [] # 将连接列表重置

        self.server.close() # 将服务端关闭
        print("连接已关闭")
        # 关闭线程
        try:
            stop_thread(self.listen_thread)
            print("线程已关闭")
        except ValueError:
            pass