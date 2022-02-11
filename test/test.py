import struct
# 3.发送数据/接受数据
data = []
with open("./data.txt",mode="r") as f:
    for line in f:
        data = line.strip("\n")
        data_len = len(data.encode("utf-8"))
        data_len = struct.pack("I",data_len)
        print(len(data_len))
   