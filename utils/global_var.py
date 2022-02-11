"""
共享变量
"""
share_vars = dict()

def _init():
    global share_vars
    # socket_status用于控制TCP服务端的状态
    share_vars["socket_status"] = False

def set_var(name,val):
    global share_vars
    try:
        share_vars[name] = val
    except Exception as e:
        print(e)

def get_var(name):
    global share_vars
    return share_vars[name]