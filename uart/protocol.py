import aioserial
from serial.serialutil import PortNotOpenError

async def data_recv_protocol(aioserial_instance):
    # 由于本人调试时单片机int为2个字节,因此首先读取2个字节的int数据作为单次发送的数据长度!
    try:
        data_len_b: bytes = await aioserial_instance.read_async(2)
    except PortNotOpenError as e:
        return
    data_len = data_len_b.decode()
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