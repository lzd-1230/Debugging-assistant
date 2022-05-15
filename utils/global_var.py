"""
共享变量
"""
share_vars = {
    "listen_ip":"0.0.0.0",
    "listen_port": 8080,
    "uart_port": "COM1",
    "baudrate": ["4800","9600","14400","19200","38400","43000","57600","76800","115200"]
}

def _init():
    global share_vars
    # socket_status用于控制TCP服务端的状态
    share_vars["socket_status"] = False

# 设置变量
def set_var(name,val):
    global share_vars
    try:
        share_vars[name] = val
    except Exception as e:
        print(e)

# 拿到变量
def get_var(name):
    global share_vars
    return share_vars[name]