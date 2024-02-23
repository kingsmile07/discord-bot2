# 作者：0x8848
# DIS：andywu#8888
# 时间:2022/3/1 20:51
import json
import random
import re
from time import sleep

import requests
from PySide6 import QtCore
from PySide6.QtCore import QThread


class reply_bot(QThread):
    _sign_quit = QtCore.Signal(type)
    _sign_del = QtCore.Signal(type)
    _sign_finished = QtCore.Signal(type)
    _sign_res1= QtCore.Signal(type)
    _sign_res2 = QtCore.Signal(type)
    _sign_res3 = QtCore.Signal(str)

    def __init__(self, ui_args):  # 导入外部传入的参数
        super(reply_bot, self).__init__()
        self.ui_args = ui_args

    def __del__(self):
        self.wait()

    def loop_args(self):
        # print(self.ui_args)
        for i in self.ui_args:
            self.text = self.ui_args[3]
            self.id_copy = self.ui_args[8]
            self.header = list(self.ui_args[6])[0]



    def run(self):
        self.loop_args()
        chanid = self.id_copy
        # rule = r"\d{18}$"
        # chanid = re.findall(rule, self.id_copy)
        header = {
            "Authorization": self.header,
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36"
        }
        # print(len(chanid))
        if len(chanid) == 18:
            channel_id =chanid
            guild_id = None
            # print(channel_id,guild_id)
            url = 'https://discord.com/api/v9/channels/{}/messages'.format(channel_id)

            msg1 = {

                "content": self.text,
                "nonce": "82329451214{}33232234".format(random.randrange(0, 1000)),
                "tts": False}
        else:
            guild_id = str(self.id_copy)[29:47]
            channel_id = str(self.id_copy)[48:66]
            message_id = str(self.id_copy)[67:85]
            url = 'https://discord.com/api/v9/channels/{}/messages'.format(channel_id)
            msg2 = {

                "content": self.text,
                "nonce": "82329451214{}33232234".format(random.randrange(0, 1000)),
                "tts": False,
                "message_reference": {"guild_id": guild_id, "channel_id": channel_id, "message_id": message_id}

            }

        if guild_id == None:
            msg = msg1
        else:
            msg = msg2

        res = requests.post(url=url, headers=header, data=json.dumps(msg))
        if res.status_code == 200:
            s = "成功"
            self._sign_res1.emit("---->信息发送%s" % s)
        else:
            s = "失败"
            self._sign_res2.emit("信息发送%s<------" % s)
