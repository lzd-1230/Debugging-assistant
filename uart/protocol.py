import aioserial
from serial.serialutil import PortNotOpenError

# 帧格式协议
async def frame_data_recv_protocol(aioserial_instance):
    """
    定义串口帧接收的协议
    模仿TCP防粘包的协议,每一次先发一个固定2Bytes的数据长度
    然后再读取相应长度的数据。
    如：
        7\r\n
        1.1 2.2
    """
    try:
        data_len_b: bytes = await aioserial_instance.read_async(2)  # 单片机中的 uint16
    except PortNotOpenError as e:
        return
    data_len = data_len_b.decode()  # 先拿到数据的长度
    # 读掉数据长度后面的回车
    _ = None
    while(_ != b'\n'):
        try:
            _ = await aioserial_instance.read_async() # win下的换行是\r\n两个字节
        except PortNotOpenError as e:
            return
    try:
        data =  await aioserial_instance.read_async(int(data_len))
    except PortNotOpenError as e:
        return
    print(f"数据:{data}")
    _ = ""
    # 读掉数据后的回车
    while(_ != b'\n'):
        try:
            _ = await aioserial_instance.read_async()
        except PortNotOpenError as e:
            return
    return data

# 行帧格式接收协议
async def rowframe_data_recv_protocol(aioserial_instance):
    data_row = await aioserial_instance.readline_async()
    return data_row


# 应用层协议:对每一帧数据进行如何拆解,python变量的定义等
def app_data_processor(data:bytes) -> list:
    """
    仅将二进制字符串序列解码并分割成数组
    如:
    b"1.1 2.2 3.3 4.4\r\n" -> ["1.1", "2.2", "3.3", "4.4\r\n"]
    """
    data = data.decode(encoding="utf8",errors="ignore")  # 这里拿到解码的数据
    # 输入: cur_data
    data_list = data.split(" ")
    return data_list

# 应用层处理:如显示到数据框和绘图区域!
def app_data_handler(widget,cur_data_list:list) -> None:
    """
    完成数据的处理和展示和画图组件交互
    widget: 为MainWindow的对象
    """
    if(int(float(cur_data_list[0])) == 0):
        key = list(widget.pic_uart.pic_dict.keys())[0]

        for i in range(1,len(cur_data_list)): 
            widget.pic_uart.data_dict[key].append(float(cur_data_list[i]))
    else: 
        key = list(widget.pic_uart.pic_dict.keys())[1]  # 滤波后的数据序列
        for i in range(1,len(cur_data_list)): 
            widget.pic_uart.data_dict[key].append(float(cur_data_list[i]))
            widget.pic_uart.cur_x += 1
        widget.pic_uart.new_data = True

    # 将数据赋值到写的窗口
    widget.ui.uart_recv_show.append(str(cur_data_list))
    if(widget.data_interact_dialog_isopened):
        widget.data_interact_dialog.ui.recv_area.append(str(cur_data_list))