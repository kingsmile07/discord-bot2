# 作者：0x8848
# DIS：andywu#8888
# 时间:2022/3/1 20:55
# 作者：0x8848
# DIS：andywu#8888
# 时间:2022/3/1 20:51
from PySide6 import QtCore
from PySide6.QtCore import QThread


class balance_bot(QThread):
    _sign_quit = QtCore.Signal(type)
    _sign_del = QtCore.Signal(type)
    _sign_finished = QtCore.Signal(type)
    _sign_res1= QtCore.Signal(type)
    _sign_res2 = QtCore.Signal(type)

    def __init__(self, ui_args):  # 导入外部传入的参数
        super(balance_bot, self).__init__()
        self.ui_args = ui_args

    def __del__(self):
        self.wait()

    def run(self):
        pass
