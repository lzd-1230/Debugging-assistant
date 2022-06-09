echo off
pyuic5 -o ui_Widget.py ./ui_files/Mywin.ui
pyuic5 -o ui_ConfigDialog.py  ./ui_files/ConfigDialog.ui
pyuic5 -o ui_RecvSendArea.py ./ui_files/Send_Recv_Area.ui
pyrcc5 -o res_rc.py .\resource\res.qrc