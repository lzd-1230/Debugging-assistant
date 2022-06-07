# -*- coding: utf-8 -*-
 
from PyInstaller.__main__ import run
import sys
 
if __name__ == '__main__':
    sys.setrecursionlimit(1000)
    opts = ['-F',
            '-w',
            '-y',
        #     '--icon=F:\Download\wallhaven-gjpqdq.png',
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
