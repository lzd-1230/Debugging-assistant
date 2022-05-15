import struct
import serial
import time
com = serial.Serial("COM2",9600)

with open("./data.txt",mode="r") as f:
    for line in f:
        data = line.strip("\n").encode("utf-8")
        data_len = len(data)
        data_len = struct.pack("I",data_len)
        com.write(data_len)
        com.write(data)
        time.sleep(0.02)