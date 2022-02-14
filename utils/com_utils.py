import socket
"""
帮忙拿到本机所有的可用ip地址,作为下拉框
"""
mode_list = ["Tcp_Server","Tcp_Client","UDP"]

def get_iplist():
    """
    获取所有本机当前可用ip
    """
    hostname = socket.gethostname()
    # 拿到列表
    ip_list = socket.gethostbyname_ex(hostname)[2]
    ip_list.append("127.0.0.1")
    ip_list.append("0.0.0.0")
    return ip_list