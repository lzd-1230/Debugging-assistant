from PyQt5.QtWidgets import QDialog
from PyQt5.Qt import QValidator
from ui_ConfigDialog import Ui_Dialog


class Uart_Config_dialog(QDialog):
    def __init__(self,):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle("串口注册")
        
    def set_init_val(self,curve_num=1,attention_range=50):
        self.ui.attention_range.setValidator(Int_Validator())
        self.ui.attention_range.setText(str(attention_range))
        self.ui.curve_num.setValue(curve_num)


    def close_return(self):
        attention_range = int(self.ui.attention_range.text())
        curve_num = self.ui.curve_num.value()
        return attention_range,curve_num

            
class Int_Validator(QValidator):
    """
    就两个方法:
        1.validate(self,输入文本,光标位置)
        2.fixup(self,)
    """
    def validate(self,input_str,curse_pos):
        if(self.finished_check(input_str)):
            return (QValidator.Acceptable, input_str,curse_pos)
        else:
            return (QValidator.Invalid, input_str,curse_pos)


    def finished_check(self,string):
        if string == "":
            return True
        try:
            int(string)
        except ValueError:
            return False
        else:
            return True



            
