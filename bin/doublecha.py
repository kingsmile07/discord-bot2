# 作者：0x8848
# DIS：andywu#8888
# 时间:2022/3/1 20:51
import json
import random
import re
import time
import traceback
from collections import deque
from time import sleep

import requests
from PySide6 import QtCore
from PySide6.QtCore import QThread


class doublecha_bot(QThread):
    _sign_res1= QtCore.Signal(type)
    _sign_res2 = QtCore.Signal(type)

    def __init__(self, ui_args):  # 导入外部传入的参数
        super(doublecha_bot, self).__init__()
        self.exit_flag3 =False
        self.ui_args = ui_args
        self.taicilist = []
        self.message_id = None
        self.talk_counter =0
        self.talk_text = 0
        self.talk_list =[]

    def __del__(self):
        print
        ">>> __del__"
    def loop_args(self):
        print("循环字典-->参数初始化")
        for i in self.ui_args:
            self.step = self.ui_args[0] #间隔时间
            self.mode = self.ui_args[4] #题词模式
            self.channels = self.ui_args[5] #激活的频道
            self.auth_list = self.ui_args[6]#账号list
            self.chaline_list = self.ui_args[9]
            self.taiciid = self.ui_args[10]

        for i in self.chaline_list:
            i = re.findall(r"\d{18}$",i)
            self.taicilist.append(i)

        self.id_list = []
        self.id2_list = []
        for item in self.channels:
            # self.id = re.findall(r"\d{18}$", item[1])
            self.id_name = item[0]
            self.id = item[1][48:]
            self.id_list.append(self.id)   #频道IDliest
            self.id2 = item[1][29:47]
            self.id2_list.append(self.id2)  #频道guild_id list
            self.header = list(self.ui_args[6])[0]
            self.guild_id = self.id2
            self.channel_id = self.id
            # print("频道ID名称：%s" % self.id_name)
            # print(self.id)
            # print(item,type(item))
        self.idslist = zip(self.id_list,self.id2_list)
    def quid(self,chanids):
        for i in self.idslist:
            if chanids == i[0]:
                guid = i[1]
                return guid
        #     print("=====================",i)
        # return [v for k, v in self.idslist if chanids in k]

    def get_keys(self, value):  # 更具值取key
        return [k for k, v in self.channels if value in v]


    def get_context(self):  # 提取指定频道的聊天内容
        for i in self.taicilist:
            print(self.taicilist[self.taiciid], type(self.taicilist[self.taiciid]))
            auth = self.header
            header = {
                "Authorization": auth,
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36"
            }
            # print("这里是cha内部调用获取语录库的函数开始")
            url = str("https://discord.com/api/v9/channels/{}/messages?limit={}".format(*self.taicilist[self.taiciid], 99))
            res = requests.get(url=url, headers=header)  # 获取随机频道的聊天内容
            # print("提取语句状态码%s" % res)
            result = json.loads(res.content)  # 通过json库的loads方法解码上面获取到的json格式为pyth的数据类型
            result_list = []
            for context in result:
                if ('<') not in context['content']:
                    if ('@') not in context['content']:
                        if ('http') not in context['content']:
                            if ('?') not in context['content']:
                                if context['content'] != "":
                                    result_list.append(context['content'])

            return random.choice(result_list)
    def get_context2(self):  # 提取指定频道的聊天内容
        # print(self.taicilist)
        # print("这里进入取词函数")
        with open("自定义台词.txt", 'r', encoding='utf-8') as f:
            for line in f.readlines():
                line = line.strip('\n')
                self.talk_list.append(line)
                if self.exit_flag3 != False:
                    break
            print("语料读取完毕,共" + str(len(self.talk_list)) + "条")
    def cha(self):


        for item in self.id_list:
            if self.exit_flag3 != False:
                break
            #   for authorization in self.auth_list:
            url = 'https://discord.com/api/v9/channels/{}/messages'.format(item)
            self.talk_counter = 0
            for authorization in self.auth_list:
                header = {
                    "Authorization": authorization,
                    "Content-Type": "application/json",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36"
                }

                msg_say = {
                    "content": self.get_context(),
                    "nonce": "82329451214{}33232234".format(random.randrange(0, 1000)),
                    "tts": False
                }
                msg_respone = {
                    "content": self.get_context(),
                    "nonce": "82329451214{}33232234".format(random.randrange(0, 1000)),
                    "tts": False,
                    "message_reference": {"guild_id": self.guild_id, "channel_id": self.channel_id,
                                          "message_id": self.message_id}
                }

                if self.message_id == None:
                    msg = msg_say
                else:
                    msg = msg_respone
                print("---url:%s\n---header:%s\n---msg:%s"%(url,header,msg))
                if self.exit_flag3 !=False:
                    break
                res = requests.post(url=url, headers=header,data=json.dumps(msg))
                result = res.json()
                print(result)
                print(res.status_code)
                self.message_id = result['id']
                self.channel_id = result['channel_id']
                self.guild_id = self.quid(item)
                self.talk_counter +=1
                if self.talk_counter >= len(self.auth_list):
                    if self.exit_flag3 != False:
                        break
                    else:
                        self.message_id =None
                else:
                    pass
                auth = authorization[0]
                name = self.get_keys(self.channel_id)
                if res.status_code == 200:
                    status = "成功"
                else:
                    status = "失败"
                dd = "账号[%s]交互模式【%s】--->发送%s"%(auth,*name,status)
                self._sign_res1.emit(dd)
                if self.exit_flag3 !=False:
                    break
                time.sleep(random.randrange(1 * self.step, 3 * self.step))
                print("="*100)
            time.sleep(random.randrange(self.step))

    def cha2(self):

        for item in self.id_list:            #   for authorization in self.auth_list:
            if self.exit_flag3 != False:
                break
            url = 'https://discord.com/api/v9/channels/{}/messages'.format(item)
            self.talk_counter = 0
            for authorization in self.auth_list:
                header = {
                    "Authorization": authorization,
                    "Content-Type": "application/json",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36"
                }

                msg_say = {
                    "content": self.talk_list[self.talk_text],
                    "nonce": "82329451214{}33232234".format(random.randrange(0, 1000)),
                    "tts": False
                }
                msg_respone = {
                    "content": self.talk_list[self.talk_text],
                    "nonce": "82329451214{}33232234".format(random.randrange(0, 1000)),
                    "tts": False,
                    "message_reference": {"guild_id": self.guild_id, "channel_id": self.channel_id,
                                          "message_id": self.message_id}
                }

                if self.message_id == None:
                    msg = msg_say
                else:
                    msg = msg_respone
                print("---url:%s\n---header:%s\n---msg:%s"%(url,header,msg))
                try:
                    res = requests.post(url=url, headers=header,data=json.dumps(msg))
                except:
                    break
                if self.exit_flag3 != False:
                    break
                self.talk_text +=1
                result = res.json()
                print(result)
                print(res.status_code)
                self.message_id = result['id']
                self.channel_id = result['channel_id']
                self.guild_id = self.quid(item)
                self.talk_counter +=1
                if self.talk_counter >= len(self.auth_list):
                    if self.exit_flag3 != False:
                        break
                    else:
                        self.message_id = None
                        continue
                else:
                    pass
                auth = authorization[0]
                name = self.get_keys(self.channel_id)
                if res.status_code == 200:
                    status = "成功"
                else:
                    status = "失败"
                dd = "账号[%s]交互模式【%s】--->发送%s"%(auth,*name,status)
                self._sign_res1.emit(dd)
                if self.exit_flag3 !=False:
                    break
                else:
                    time.sleep(random.randrange(1 * self.step, 3 * self.step))
                    continue
                print("="*100)


    def run(self):
        print("进入send线程中了")
        self.loop_args()
        if self.mode == True:  # 这里是随机提取模式
            print("交互聊天-提取台词")
            while self.exit_flag3 != True:
                try:
                    self.cha()
                except:
                    pass
            self._sign_res2.emit("交互聊天:提取---->线程已经停止".center(50, "-"))

        else:  # 这里是自定义台词模式
            print("交互聊天-自定义台词")
            while self.exit_flag3 != True:
                self.get_context2()
                try:
                    self.cha2()
                except:
                    pass
            self._sign_res2.emit("交互聊天:自定---->线程已经停止".center(50, "-"))


