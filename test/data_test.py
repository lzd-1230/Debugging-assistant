import socket
import time
import random
import struct


def main():
    data_num = 5
    # 构造数据
    with open("./data.txt",mode="w") as f:
        for i in range(2000):
            for j in range(data_num): # 设置曲线量
                data = round(1000*random.random(),2)
                if(j<data_num):
                    f.write(str(data)+" ")
                else:
                    f.write(str(data))
            f.write("\n")
     # 1.创建TCP套接字
    tcp_client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)  # tcp套接字
    # 2.连接服务器
    server_ip = "127.0.0.1"
    server_port = 8080
    server_addr = (server_ip,server_port)
    
    tcp_client_socket.connect((server_ip,server_port))



    # 3.发送数据/接受数据
    with open("./data.txt",mode="r") as f:
        for line in f:
            data = line.strip("\n").encode("utf-8")
            data_len = len(data)
            data_len = struct.pack("I",data_len)
            tcp_client_socket.send(data_len)
            tcp_client_socket.send(data)
            time.sleep(0.02)
    print("发送完成")
    # 4.关闭套接字
    tcp_client_socket.close()

if __name__ == "__main__":
    main()