echo off
pyuic5 -o ui_Widget.py ./Mywin.ui
pyrcc5.exe .\res.qrc -o res_rc.py