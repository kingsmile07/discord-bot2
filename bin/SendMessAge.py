# 作者：0x8848
# DIS：andywu#8888
# 时间:2022/3/1 20:51
import json
import random
import re
import time
from collections import deque
from time import sleep

import requests
from PySide6 import QtCore
from PySide6.QtCore import QThread


class send_bot(QThread):
    _sign_res1 = QtCore.Signal(type)
    _sign_res2 = QtCore.Signal(type)

    def __init__(self, ui_args):  # 导入外部传入的参数
        super(send_bot, self).__init__()
        self.ui_args = ui_args
        self.taicilist = []
        self.exit_flag2 =False

    def __del__(self):
        print
        ">>> __del__"

    def loop_args(self):
        print("进入loop了")
        print("ui参数", self.ui_args)
        for i in self.ui_args:
            self.step = self.ui_args[0]
            self.timeline = self.ui_args[1]
            self.numb = self.ui_args[2]
            self.mode = self.ui_args[4]
            self.channels = self.ui_args[5]
            self.auth_list = self.ui_args[6]
            self.keywords = self.ui_args[7]
            self.cout = 0
            self.chaline_list = self.ui_args[9]
            self.taiciid = self.ui_args[10]
            # self.chaline_list = str(self.ui_args[9])[-21:-3]  #提取台词频道ID
        #     # re.findall(r"\d{18}$",self.chaline_list)
        # print(type(self.chaline_list),str(self.ui_args[9])[-21:-3])
            # self.taicilist = re.findall(r"\d{18}$",self.chaline_list)
        for i in self.chaline_list:
            i = re.findall(r"\d{18}$",i)
            self.taicilist.append(i)

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
        return [k for k, v in self.channels if value in v]

    def get_context(self):  # 提取指定频道的聊天内容
        # print(self.taicilist)
        # print("这里进入取词函数")
        for i in self.taicilist:
            # print(self.taicilist[self.taiciid],type(self.taicilist[self.taiciid]))
            auth = self.header
            header = {
                "Authorization": auth,
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36"
            }
            # print("这里是cha内部调用获取语录库的函数开始")
            url = str("https://discord.com/api/v9/channels/{}/messages?limit={}".format(*self.taicilist[self.taiciid], 99))
            # print(i, auth, url, header)
            res = requests.get(url=url, headers=header)  # 获取随机频道的聊天内容
            print("提取语句状态码%s" % res)
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



    def get_context_rodom(self):
        with open("自定义台词.txt", 'r', encoding='utf-8') as f:
            data = f.readlines()
            context_list = data
            text = random.choice(data)
            used = deque(maxlen=1000)
            text = random.choice([x for x in context_list if x not in used])  # 随机选择一条没有在used中的信息。
            used.append(text)
            while len(used) > 1000:
                text = used.popleft()
                print("内容：%s" % text)

            return text

    def cha(self):  # 提取指定频道的聊天内容
        print("cha1开始发送指定频道的聊天内容")
        auth_cout = 0
        try:
            for i in self.id_list:
                # print("------------------>到这里了")
                status_arg = []

                for auth in self.auth_list:
                    msg = {

                        "content": self.get_context(),
                        "nonce": "82329451214{}33232234".format(random.randrange(0, 1000)),
                        "tts": False

                    }
                    header = {
                        "Authorization": auth,
                        "Content-Type": "application/json",
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36"
                    }
                    print("----------------当前发送链接：\n%s\n--->%s\n%s"%(i,auth,header))
                    auth_cout +=1
                    url = 'https://discord.com/api/v9/channels/{}/messages'.format(i)
                    res = requests.post(url=url, headers=header, data=json.dumps(msg))
                    if self.exit_flag2 != False:
                        break
                    print(res.status_code)
                    name = self.get_keys(i)
                    if res.status_code == 200:
                        status = "成功"
                        self.cout += 1
                    else:
                        status = "失败"
                    # print("发送信息状态码：%s" % s)
                    # print("-" * 100)
                    dd = "【群发】[%s]【%s】发送%s-共%s条信息成功发送" %(auth[0], *name,status,self.cout)
                    print("账号%s向频道%s发送%s"%(auth[0],*name,status))
                    print("=" * 100)
                    self._sign_res1.emit(str(dd))

                    if self.exit_flag2 != False:
                        break
                    else:
                        time.sleep(random.randrange(1 * self.step, 3 * self.step))  # 每条信息发送后暂停时间
                        continue
                if self.exit_flag2 != False:
                    break
                else:
                    time.sleep(self.step) #频道列表跑完后暂停时间
                    continue


        except:
            pass

    def cha2(self):  # 提取指定频道的聊天内容
        print("cha2开始发送指定频道的聊天内容")
        auth_cout = 0
        try:
            for i in self.id_list:
                # print("------------------>到这里了")
                status_arg = []
                for auth in self.auth_list:
                    msg = {

                        "content": self.get_context_rodom(),
                        "nonce": "82329451214{}33232234".format(random.randrange(0, 1000)),
                        "tts": False

                    }
                    header = {
                        "Authorization": auth,
                        "Content-Type": "application/json",
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36"
                    }
                    print("----------------当前发送链接：\n%s\n--->%s\n%s"%(i,auth,header))
                    auth_cout +=1
                    url = 'https://discord.com/api/v9/channels/{}/messages'.format(i)
                    print(url)
                    res = requests.post(url=url, headers=header, data=json.dumps(msg))
                    print(res.status_code)
                    if self.exit_flag2 != False:
                        break
                    print(res.status_code)
                    name = self.get_keys(i)
                    if res.status_code == 200:
                        status = "成功"
                        self.cout += 1
                    else:
                        status = "失败"
                    # print("发送信息状态码：%s" % s)
                    # print("-" * 100)
                    dd = "账号[%s]【%s】发送%s-共%s条信息成功发送" %(auth[0], *name,status,self.cout)
                    print("账号%s向频道%s发送%s"%(auth[0],*name,status))
                    print("=" * 100)
                    # status_arg.append("账号：%s"%auth1)
                    # status_arg.append("频道%s："%name)
                    # status_arg.append(dd)
                    self._sign_res1.emit(str(dd))

                    if self.exit_flag2 != False:
                        break
                    else:
                        time.sleep(random.randrange(1 * self.step, 3 * self.step))  # 每条信息发送后暂停时间
                        continue
                if self.exit_flag2 != False:
                    break
                else:
                    time.sleep(self.step)  # 频道列表跑完后暂停时间
                    continue



        except:
            pass

    def run(self):
        print("进入send线程中了")
        self.loop_args()
        if self.mode == True:  # 这里是随机提取模式
            print("这里是随机模式")
            while self.exit_flag2 != True:
                # print("------------------>到这里了")
                try:
                    self.cha()
                except:
                    pass
            self._sign_res2.emit("发送消息[提取模式]线程已经停止".center(50, "-"))
        else:  # 这里是自定义台词模式
            while self.exit_flag2 != True:
                # print("------------------>到这里了")
                try:
                    self.cha2()
                except:
                    pass
            self._sign_res2.emit("发送消息[自定模式]线程已经停止".center(50, "-"))
        # while self.exit_flag2 != True:
        #
        # self._sign_res2.emit("发送线程已经停止".center(50,"-"))
