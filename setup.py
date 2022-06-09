# -*- coding: utf-8 -*-
 
from PyInstaller.__main__ import run
import sys
import os

if __name__ == '__main__':
    sys.setrecursionlimit(1000)
    if os.name == "nt":
        opts = ['-F',
                '-w',
                '-y',
                # '--icon=./image/avartar.ico',
                # '--paths=D:\\ProgramData\\Anaconda3\\Lib\\site-packages\\PyQt5\\Qt\\bin',
                # '--paths=D:\\ProgramData\\Anaconda3\\Lib\\site-packages\\PyQt5\\Qt\\plugins',
                # '--paths=D:\\ProgramData\\Anaconda3\\Lib\\site-packages\\newspaper3k-0.2.6-py3.6.egg\\newspaper',
                '--add-data', '.\style.qss;.\style.qss',
                '--add-data', '.\config\*;.\config',
                # '--add-data', 'image/*;image/',
                '--add-data', '.\data_save\*;.\data_save',
                # '--clean',
                # '--icon=icon\\icon.ico',
                'main.py']
    elif os.name=="posix":  # 好像不太行,pyqtgraph的包好像要手动引入了...
        opts = ['-F',
                '-y',
                '--icon=./image/avartar.png',
                # '--paths=D:\\ProgramData\\Anaconda3\\Lib\\site-packages\\PyQt5\\Qt\\bin',
                # '--paths=D:\\ProgramData\\Anaconda3\\Lib\\site-packages\\PyQt5\\Qt\\plugins',
                # '--paths=D:\\ProgramData\\Anaconda3\\Lib\\site-packages\\newspaper3k-0.2.6-py3.6.egg\\newspaper',
                # '--add-data', './style.qss;./style.qss',
                # '--add-data', 'config/*;config/',
                # '--add-data', 'image/*;image/',
                # '--add-data', 'data_save/;data_save/',
                # '--clean',
                # '--icon=icon\\icon.ico',
                'main.py']
    run(opts)
