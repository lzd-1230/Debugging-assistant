import asyncio
import aioserial
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QFont, QTextCursor
from PyQt5.QtCore import Qt
from quamash import QEventLoop
import serial.tools.list_ports


# from asyncio import ensure_future as aioasync

class Gui(QWidget):
    def __init__(self, loop, parent=None, **kwargs):
        super(__class__, self).__init__(**kwargs)
        self.loop = loop    # 事件循环
        self.resize(400, 300)
        self.setWindowTitle('Garbage Chat')
        self.maxlines = 15
        self.initialize()
        self.show()   # 事件循环一定要放在show后面???

    # def send(self, *obj):
    #     self.client.send(self.userInput.text())
    #     self.userInput.setText("")

    # 收到数据后的回调函数!!!!
    def output(self, data):
        self.outTE.insertPlainText(data)
        self.set_text_cursor_pos(-1)
            
    def initialize(self):
        
        userlabel = QLabel("lzd", self)
        userlabel.move(5,5)
        userlabel.setStyleSheet("color:#444444; font-size: 15px;")
        
        self.outTE = QTextEdit("", self)
        self.outTE.setReadOnly(True)
        self.outTE.setMouseTracking(True)
        self.outTE.resize(362,200)
        self.outTE.textSelected = False
        self.outTE.move(25,37)

        sendButton = QPushButton("Send")
        # sendButton.clicked.connect(self.send)

        userInput = QLineEdit(self)
        userInput.setStyleSheet("background: white; width:300px; border:2px solid #444444; font-size: 13px;")
        self.userInput = userInput
        
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(userInput)
        hbox.addWidget(sendButton)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()
        if e.key() == Qt.Key_Return:
            self.send()

    def get_text_cursor(self):
        return self.outTE.textCursor()

    def set_text_cursor_pos(self, value):
        tc = self.get_text_cursor()
        tc.setPosition(value, QTextCursor.KeepAnchor)
        self.outTE.setTextCursor(tc)

    def get_text_cursor_pos(self):
        return self.get_text_cursor().position()
            
class App(QApplication):
    def __init__(self):
        QApplication.__init__(self,[])
        loop = QEventLoop(self)  # 事件循环
        print(loop)
        self.loop = loop
        asyncio.set_event_loop(self.loop) 
        self.serial = aioserial.AioSerial(port='COM2', baudrate=9600,loop=self.loop) # 这里让AioSerial作为你的
        loop.create_task(self.start()) 
        
        self.gui = Gui(self.loop,)  # 创建界面,并在界面中运行事件循环!
        loop.run_forever()  # 这里直接接管你的QT程序!
    
    # 异步任务
    async def read_and_print(self,aioserial_instance: aioserial.AioSerial):
        while True:
            data: bytes = await aioserial_instance.read_async() # 
            print(data.decode(errors='ignore'), end='', flush=True)
            # 停止读取数据的方式!
            # if b'\n' in data:
            #     aioserial_instance.close()  # 每次读到换行之后就结束这一次异步任务
            #     break

    async def start(self):
        coro = self.read_and_print(self.serial)
        self.loop.create_task(coro)

if __name__ == "__main__":
    App()
