# 作者：0x8848
# DIS：andywu#8888
# 时间:2022/3/1 20:51
import datetime
import json
import threading
import time
from time import sleep
from typing import re

import requests
from PySide6 import QtCore
from PySide6.QtCore import QThread


class monitor_bot(QtCore.QObject):
    _sign_res1 = QtCore.Signal(type)
    _sign_res2 = QtCore.Signal(type)
    _sign_res3 = QtCore.Signal(type)
    _sign_res4 = QtCore.Signal(type)
    _sign_res5 = QtCore.Signal(type)
    _sign_res6 = QtCore.Signal(type)
    _sign_res7 = QtCore.Signal(type)

    def __init__(self, ui_args):  # 导入外部传入的参数
        super(monitor_bot, self).__init__()
        self.ui_args = ui_args
        self.exit_flag =False

    def __del__(self):
        print
        ">>> __del__"


    def loop_args(self):
        # print(self.ui_args)
        for i in self.ui_args:
            self.step = self.ui_args[0]
            self.timeline = self.ui_args[1]
            self.numb = self.ui_args[2]
            self.channels = self.ui_args[5]
            self.auth_list = self.ui_args[6]
            self.keywords = self.ui_args[7]

        self.id_list = []
        for item in self.channels:
            # self.id = re.findall(r"\d{18}$", item[1])
            self.id_name = item[0]
            self.id = item[1][48:]
            self.id_list.append(self.id)
            # print("频道ID名称：%s" % self.id_name)
            # print(self.id)
            # print(item,type(item))

    def get_keys(self,value):  # 更具值取key
        return [k for k, v in self.channels if value in v]

    def get_time(self,date):  # 传入2个参数 消息的时间戳和设置的 时效性
        # print("这是在时间处理函数中的信息")
        # print(date,type(date))
        update = date[0:19].replace('T', ' ')
        # print(update)
        utc_date = datetime.datetime.strptime(update, "%Y-%m-%d %H:%M:%S")
        local_date = utc_date + datetime.timedelta(hours=8)  # 消息的UTC时间  转 本地时间
        local_now = str(datetime.datetime.now())[0:16]  # 获取本地当前时间
        local_time = datetime.datetime.strptime(local_now, "%Y-%m-%d %H:%M")
        offset1 = (local_time - local_date).seconds
        offset2 = ((local_time - local_date).days) * 24 * 60 * 60
        timeX = int((offset1 + offset2) / 60 / 60)  # 消息发送时间距离现在时间的差（小时）
        # print("信息发布的本地时间",local_date)
        # print("距离当前时间",timeX)
        # print("timex-------------",timeX)
        if timeX > int(self.timeline):
            flag = False
        else:
            flag = True

        return flag,local_date

    def Assemble_links(self, value):
        # print(self.channels,value)
        for item in self.channels:
            if item[0] in value:
                return item[1]

    def keyword_func(self,listitem):  # 关键字检查
        return (True,listitem) if any(i in listitem for i in self.keywords) else (False,listitem)


    def keyword_func2(self,content):
        if content in self.duplicates_list: #在重复列表中
            # print("重复的---------------》%s" % content)
            return None
        else:
            self.duplicates_list.append(content)
            # print("不重复的--》%s"% content)
            sleep(0.1)
            return self.keyword_func(content)


    def run(self):
        print("Monitor线程的-->name：%s | ID：%s" % (threading.current_thread().name, threading.current_thread().ident))
        self.loop_args()
        # print("频道ID列表",self.id_list)
        print(self.auth_list)
        # print(self.channels,type(self.channels))
        auth_cout = 1
        id_cout = 0
        self.duplicates_list =[]
        while self.exit_flag != True:
            header = {
                "Authorization": list(self.auth_list)[0],
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36"
            }
            for id in self.id_list:
                tem_url = str("https://discord.com/api/v9/channels/{}/messages?limit={}".format(id, self.numb))
                try:
                    res = requests.get(url=tem_url, headers=header, timeout=5)
                    result = json.loads(res.content)  # 这里获取了一个频道的结果
                    result = list(reversed(result))
                    # print(type(result))
                    solt = "---【第%s轮次-第%s个频道】：%s\n 状态码：%s" % (auth_cout,id_cout, id, res.status_code)
                    self._sign_res7.emit(solt)
                    # temp_list = []  # 声明一个list，用来存放每个频道提取的信息
                    for contents in result:  # 从结果中获取元素
                        # print(contents)
                        # print(contents.get("timestamp"))

                        if type(contents) == dict:

                            # print(contents,type(contents))
                            timestamp = contents.get("timestamp")
                            # print(timestamp)
                            temp_time = self.get_time(str(timestamp))
                            #
                            # print(temp_time,type(temp_time))
                            #
                            # print("----------------------我到这里了")
                            if temp_time[0] == True: #符合时间

                                timestamp = temp_time[1]
                                # print("----------------------我到这里了")
                                id = contents.get("id")
                                content = contents.get("content").replace("<@!883922174644224043>", "@andywu-| ")
                                channel_notes = str(self.get_keys(contents.get("channel_id"))).replace("['","").replace("']","")
                                username = contents.get("author")["username"][0:5]
                                sms_link = str(self.Assemble_links(channel_notes))+"/"+id
                                # temp_item = """【%s】频道-->%s\n【%s】说:---->%s\n%s\n-------------------------------------""" % (
                                #     channel_notes, timestamp, username, content, sms_link)
                                # # temp_list.append(temp_item)
                                # temp_list.insert(0, temp_item)  # 获取的元素插入list 计数
                                # print(temp_item)
                                dd =self.keyword_func2(content)

                                if dd != None:  #不含关键字
                                    if dd[0] == True:
                                        sms1 = """【%s】频道-->%s """ % (channel_notes, timestamp)
                                        self._sign_res4.emit(sms1)
                                        sms2 = """【%s】说:---->%s""" % (username, dd[1])
                                        self._sign_res5.emit(sms2)
                                        sms3 = """%s""" % sms_link
                                        self._sign_res6.emit(sms3)
                                    else:
                                        sms1 = """【%s】频道-->%s """ % (channel_notes, timestamp)
                                        self._sign_res1.emit(sms1)
                                        sms2 = """【%s】说:---->%s""" % (username, dd[1])
                                        self._sign_res2.emit(sms2)
                                        sms3 = """%s""" % sms_link
                                        self._sign_res3.emit(sms3)
                                        pass
                                else:
                                    pass
                            else:   #不符合时间
                                pass
                        else:
                            pass
                    if self.exit_flag == False:
                        id_cout += 1
                        continue
                    else:
                        break
                except:
                    #self._sign_res1.emit(result)
                    continue
            auth_cout+=1
            id_cout =0
        pass



