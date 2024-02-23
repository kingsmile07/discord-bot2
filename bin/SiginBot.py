# 作者：0x8848
# DIS：andywu#8888
# 时间:2022/3/1 20:51
import json
import random
import re
import time

import requests
from PySide6 import QtCore
from PySide6.QtCore import QThread


class sigin_bot(QThread):
    _sign_quit = QtCore.Signal(type)
    _sign_del = QtCore.Signal(type)
    _sign_finished = QtCore.Signal(type)
    _sign_res1= QtCore.Signal(type)
    _sign_res2 = QtCore.Signal(type)

    def __init__(self, ui_args):  # 导入外部传入的参数
        super(sigin_bot, self).__init__()
        self.ui_args = ui_args

    def __del__(self):
        self.wait()

    def loop_args(self):
        print("进入loop了")
        print("ui参数", self.ui_args)
        for i in self.ui_args:
            self.step = self.ui_args[0]
            self.timeline = self.ui_args[1]
            self.numb = self.ui_args[2]
            self.text = self.ui_args[3]
            self.mode = self.ui_args[4]
            self.channels = self.ui_args[5]
            self.auth_list = self.ui_args[6]
            self.keywords = self.ui_args[7]
            self.cout = 0
            self.chaline_list = self.ui_args[9]
            # self.chaline_list = str(self.ui_args[9])[-21:-3]  #提取台词频道ID
        #     # re.findall(r"\d{18}$",self.chaline_list)
        # print(type(self.chaline_list),str(self.ui_args[9])[-21:-3])
            # self.taicilist = re.findall(r"\d{18}$",self.chaline_list)
        # for i in self.chaline_list:
        #     i = re.findall(r"\d{18}$",i)
        #     self.taicilist.append(i)
        #     print("------------到这里了")



        # print("-----------》提",i)

        self.id_list = []
        for item in self.channels:
            # self.id = re.findall(r"\d{18}$", item[1])
            self.id_name = item[0]
            self.id = item[1][48:]
            self.id_list.append(self.id)
            self.header = list(self.ui_args[6])[0]
            # print("频道ID名称：%s" % self.id_name)
            # print(self.id)
            # print(item,type(item))

    def get_keys(self, value):  # 更具值取key
        # print("--------------",value)
        # print("------------",self.channels)
        return [k for k, v in self.channels if value in v]

    def run(self):
        print("签到run开始")
        def cha():  # 提取指定频道的聊天内容
            print(self.auth_list)
            for authorization in self.auth_list:

                header = {
                    "Authorization": authorization,
                    "Content-Type": "application/json",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36"
                }
                for chanel_id in self.id_list:
                    msg = {

                        "content": str(self.text),
                        "nonce": "82329451214{}33232234".format(random.randrange(0, 1000)),
                        "tts": False

                    }

                    url = 'https://discord.com/api/v9/channels/{}/messages'.format(chanel_id)

                    try:
                        res = requests.post(url=url, headers=header, data=json.dumps(msg))
                        auth =authorization[0:1]
                        name =str(self.get_keys(chanel_id))[2:-2]
                        print(name)
                        print(url,header,msg)

                        if res.status_code == 200:

                            self._sign_res1.emit("【%s】在[%s]频道--->签到成功"% (auth,name))
                            time.sleep(self.step)
                        else:

                            self._sign_res1.emit("【%s】在[%s]频道--->签到失败"% (auth,name))
                            time.sleep(self.step)
                        print(res.status_code)
                    except:
                        pass

        self.loop_args()
        cha()
        pass
