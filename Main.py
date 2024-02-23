# 时间:2022/3/1 20:49
import hashlib
import os
import sys
import this

# import pywintypes

from PySide6.QtCore import QStringListModel, QFile, QIODevice
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QMainWindow, QMessageBox, QPlainTextEdit, QTableView
from bin.Monitor import *
from bin.ReplyShortcut import *
from bin.SendMessAge import *
from bin.SiginBot import *
from bin.balance import *
from bin.doublecha import *
from ui_toolsbox import *


class BoxMain(QMainWindow, Ui_Form):  # Ui_MainWindow 为自动生成的PY文件的类名
    _startThread = QtCore.Signal()
    _startThread2 = QtCore.Signal()
    _startThread3 = QtCore.Signal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)  # 调用ui界面
        self.load_ui()
        self.setWindowTitle("Andy|中文社区 | Dis：AndyWu#6508")
        # filepath = "E:\\pythonProject\\tool\\ui\\MessageBox.ui"
        # self.dialog = QUiLoader().load(filepath)
        self.Thread_monitor = QThread(self)
        self.Thread_monitor2 = QThread(self)
        self.Thread_send = QThread(self)
        self.Thread_doublecha = QThread(self)
        self.dialog.tableView_dict = QTableView()
        self.print_5 = QPlainTextEdit(self)
        self.print_5.setStyleSheet("background-color:rgba(32,34,37,1.00);")
        self.print_5.move(5, 395)
        self.print_5.resize(976, 236)
        self.print_5.setReadOnly(True)
        self.print_5.lower()

        self.print_3 = QPlainTextEdit(self)
        self.print_3.setStyleSheet("background-color:rgba(32,34,37,1.00);")
        self.print_3.move(490, 125)
        self.print_3.resize(491, 226)
        self.print_3.setReadOnly(True)
        self.print_5.lower()
        #
        # self.print_6 = QPlainTextEdit(self)
        # self.print_6.move(115,105)
        # self.print_6.resize(371,71)

        self._initWindow()
        self._initArgs()  # 初始化字典和参数

    def load_ui(self):
        # path = os.path.realpath(os.curdir)  # 获取当前目录的绝对路径
        # self.ui = QUiLoader().load(path + '/ui/main.ui')
        abs_dir = os.path.abspath(os.path.dirname(__file__))
        ui_file_name = abs_dir+r"\MessageBox.ui"
        print("ui_file_name",ui_file_name)
        ui_file = QFile(ui_file_name)
        if not ui_file.open(QIODevice.ReadOnly):
            print("Cannot open {}: {}".format(ui_file_name, ui_file.errorString()))
            sys.exit(-1)
        loader = QUiLoader()
        self.dialog = loader.load(ui_file)
        ui_file.close()
        if not self.dialog:
            print(loader.errorString())
            sys.exit(-1)

    # Ui窗口信号初始化
    def _initWindow(self):
        print("主线程的-->name：%s | ID：%s" % (threading.current_thread().name, threading.current_thread().ident))
        self.but_exit.clicked.connect(self._exit)  # 退出程序按钮
        self.but_add_config.clicked.connect(self.add_config_click)  # 添加配置按钮信号槽
        self.but_save_config.clicked.connect(self.save_config_click)  # 保存按钮信号槽
        self.but_del_dict.clicked.connect(self.del_dict)  # 删除按钮信号槽
        self.but_red_config.clicked.connect(self.check_file)  # 读取配置按钮信号槽
        self.input_shortcut.setText("GM")
        self.chk_taici.clicked.connect(self.check_box)
        self.cmbox_activation.textActivated.connect(self.active_lists)
        self.cmbox_config.textActivated.connect(self.moddif_label)
        self.cmbox_revise.textActivated.connect(self.Modify_dict)
        self.dialog.listView_dict.doubleClicked.connect(self.del_keyworditem)
        self.but_add_config_key.clicked.connect(self.add_config_key)
        # self.dialog.tableView_dict.doubleClicked.connect(self.del_keyworditem)
        self.but_cls_kwsms.raise_()
        self.chk_translate.clicked.connect(self.check_t)
        # self.dialog.listView_dict.clicked.connect(self.prt_item)
        self.label_7.setText("<a style='color: green;' href=\"https://discord.gg/mMGgpmKEgg\">加入社区")

        self.but_del_key1.clicked.connect(self.del_key)
        self.but_monitor.clicked.connect(self.start)
        self.but_monitor2.clicked.connect(self.start2)
        self.but_shortcut.clicked.connect(self.func_but_shortcut)
        self.but_cls_logtotext_2.clicked.connect(self.func_but_clear4)
        self.but_cls_kwsms.clicked.connect(self.func_but_clear3)
        self.but_send.clicked.connect(self.start_send)
        self.pushButton_11.clicked.connect(self.func_but_taici)
        self.but_daiban.clicked.connect(self.func_but_daiban)
        self.but_double_cha.clicked.connect(self.start_doublecha)
        self.but_more.clicked.connect(self.check_t)
        self.spinBox_setp.setValue(5)
        self.spinBox_numb.setValue(10)
        self.spinBox_time.setValue(4)
        # self.but_pause.clicked.connect(self.start)

        self.but_sign.clicked.connect(self.func_but_sign)
        self.chk_taici.setCheckState(Qt.Checked)
        self.chk_taici.setText("提取台词")


    def moddif_label(self):  # 设置配置去的控件标签动作
        self.combox_select = self.cmbox_config.currentText()
        self.dictkey = self.text_key.text()
        self.dictvalue = self.text_value.text()
        if self.combox_select == "代理设置":
            self.label_value.setEnabled(False)
            self.text_value.setEnabled(False)
            self.text_value.setPlaceholderText("")
            self.text_key.setPlaceholderText("例：http://127.0.0.1:7890")
        elif self.combox_select == "关键字表":
            self.label_value.setEnabled(False)
            self.text_value.setEnabled(False)
            self.text_value.setPlaceholderText("")
            self.text_key.setPlaceholderText("每次只能添加一个关键词")
        elif self.combox_select == "授权账号":
            self.label_value.setEnabled(True)
            self.text_value.setEnabled(True)
            self.text_value.setPlaceholderText("填authorization值，打开网页版discord，按F12可以查看")
            self.text_key.setPlaceholderText("账号名称可以随意备注")
        else:
            self.label_value.setEnabled(True)
            self.text_value.setEnabled(True)
            self.label_key.setText("频道名称")
            self.text_value.setPlaceholderText("复制频道网址填入")
            self.text_key.setPlaceholderText("频道名称可以随意备注")

        pass

    # -----------------------------------------------------------------全局参数初始化

    def _initArgs(self):  # 全局参数初始化
        self.check_file()  # 检查文件是否存在
        # self.dict_con = {}  # 配置字典
        self.activa_list = []  # 当前激活的list
        # self.chaline_list = []  # 提取台词的频道
        # self.auths_list = []  # 账号授权list
        # self.keyword_list = []  # 关键字list
        self.ui_args = []  # 界面UI参数组

    def loop_dict(self):  # 初始化字典 提取基本参数
        for item in self.dict_con:
            if item == "授权账号":
                if self.chk_id.isChecked() != True:
                    self.auths_list = self.dict_con.get("授权账号").values()
                    self.cmbox_revise.addItem(item)
                    print(self.auths_list)
                else:
                    self.auths_list = list(self.dict_con.get("授权账号").values())[0]
                    self.auths_list = self.auths_list.split("没有")
                    self.cmbox_revise.addItem(item)
                    print(self.auths_list)
            elif item == "关键字表":
                self.keyword_list = self.dict_con.get("关键字表")
                self.cmbox_revise.addItem(item)
            elif item == "代理设置":
                self.proxy = self.dict_con.get("代理设置")[0]
                os.environ["http_proxy"] = self.proxy
                os.environ["https_proxy"] = self.proxy
                self.cmbox_revise.addItem(item)
            elif item == "提词专用":
                self.chaline_list = self.dict_con.get("提词专用").values()
                self.cmbox_revise.addItem(item)
            else:
                self.cmbox_revise.addItem(item)
                self.cmbox_activation.addItem(item)



        # print("授权账号",type(self.auths_list),self.auths_list)
        # print("关键字表",type(self.keyword_list),self.keyword_list)
        # print("代理设置", type(self.proxy), self.proxy)
        # print("提取台词", type(self.chaline_list), self.chaline_list)

        self.moddif_label()

    def active_args(self):  # 获取界面参数
        self.cmbox_revise.clear()
        self.cmbox_activation.clear()
        self.loop_dict()
        self.print_2.clear()
        self.print_2.append(str(self.keyword_list))
        self.check_box()
        if self.print_3.textCursor().selectedText() == "":
            self.id_copy = self.print_5.textCursor().selectedText()
        else:
            self.id_copy = self.print_3.textCursor().selectedText()

        self.setp = self.spinBox_setp.value()
        self.timeline = self.spinBox_time.value()
        self.smsNumb = self.spinBox_numb.value()
        self.shortcut = self.input_shortcut.text()
        self.taiciid = self.spinBox_quci.value()
        self.ui_args = [self.setp, self.timeline, self.smsNumb, self.shortcut, self.mode, self.activa_list,
                        self.auths_list, self.keyword_list, self.id_copy, self.chaline_list,self.taiciid]
        self.ui_args_text = (
                "间隔时间：%s \n信息时效：%s\n提取条数：%s\n快捷文本：%s\n台词模式：%s\n激活频道：%s\n授权账号：%s\n关键字：%s\n快捷ID：%s\n提词频道：%s" % (
            self.setp, self.timeline, self.smsNumb, self.shortcut, self.mode, self.activa_list, self.auths_list,
            self.keyword_list, self.id_copy, self.chaline_list))

        # print("间隔时间：%s --信息时效：%s------提取条数：%s-----快捷文本：%s---台词模式：%s" % (
        #     self.setp, self.timeline, self.smsNumb, self.shortcut, self.mode))
        print("-----------------------------以下信息来自Main-->active_args()")
        print(self.ui_args_text)
        print("-----------------------------以上信息来自Main-->active_args()")
        # print(self.ui_args)

    def check_box(self):
        if self.chk_taici.isChecked() == True:
            self.chk_taici.setText("提取台词")

            self.mode = True

        else:
            self.mode = False
            self.chk_taici.setText("自备台词")

    def check_t(self):
        if self.chk_translate.isChecked()== True:
            self.chk_translate.setText("中-->英")
            source_text =self.source_text()
            source1 = "zh"
            source2 = "en"
        else:
            self.chk_translate.setText("英-->中")
            source_text = self.source_text()
            source1 = "en"
            source2 = "zh"
        if source_text == "":
            print("没有内容需要翻译")
        else:
            self.result = self.translate(source_text,source1,source2)
            self.print_2.append("内容翻译结果".center(80,"-"))
            self.print_2.append(str(self.result))




    def source_text(self):
        if self.print_3.textCursor().selectedText() == "":
            source_text = self.print_5.textCursor().selectedText()
        else:
            source_text = self.print_3.textCursor().selectedText()
        return source_text

    def translate(self,source_text, source1, source2):
        appid = '20220305001111252'  # 你的appid
        secretKey = 'aEwTsuUhdWfvV7dJRBu0'  # 你的密钥
        salt = str(random.randint(0, 50))

        sign = appid + source_text+ salt + secretKey
        sign = hashlib.md5(sign.encode(encoding='UTF-8')).hexdigest()
        head = {'q': source_text,
                'from': source1,
                'to': source2,
                'appid': appid,
                'salt': salt,
                'sign': sign}

        res = requests.get('http://api.fanyi.baidu.com/api/trans/vip/translate', head)
        result = res.json()
        result = ((result.get("trans_result")[0]).get("dst"))
        return result


    def active_lists(self):
        activeKEY = self.cmbox_activation.currentText()
        for item in self.dict_con:
            if item == activeKEY:
                self.activa_list = self.dict_con.get(item).items()
                # print(type(self.dict_con.get(item).items()),self.dict_con.get(item).items())
                self.print_1.append("当前激活的频道--->%s" % activeKEY)
                msg =str([x for x,y in self.dict_con.get(item).items()])
                msg = """<span style="color: rgba(255,162,29,1.00); padding-left: 10px; padding-right: 14px; 
                        font-size: 13px;">%s</span></br>""" % msg
                self.print_5.clear()
                self.print_5.appendHtml(msg)
                return self.activa_list

    # -----------------------------------------------------------------全局参数初始化

    def check_file(self):
        self.dict_con ={}
        try:
            f = open('config.json')
            self.read_config()
            self.loop_dict()
            self.spinBox_quci.setMaximum(len(self.dict_con.get("提词专用"))-1)
        except:
            QMessageBox.information(self, "欢迎使用",
                                    "软件功能：\n1：监控关注频道的信息\n2：干白名单交互聊天\n3：指定频道每日自动签到\n\n！没有发现配置，请先添加配置文件并保存\n  ")
            self.print_1.clear()
            self.print_1.append("软件功能：\n1：监控关注频道的信息\n2：干白名单交互聊天\n3：指定频道每日自动签到\n4：欢迎定制（Dis：AndyWu#6508） ")
            pass
        finally:
            pass


    # -----------------------------------------------------------------菜单按钮区
    #添加字典键值
    def add_config_key(self):
        key = self.text_key.text()
        self.cmbox_config.addItem(key)
        self.print_1.append("%s-已经添加到列表"%key)


    # 添加字典项目
    def add_config_click(self):
        choose = QMessageBox.information(self, "重要提醒！！！", "确认添加", QMessageBox.Yes | QMessageBox.No)
        if choose == 16384:
            self.combox_select = self.cmbox_config.currentText()
            self.dictkey = self.text_key.text()
            self.dictvalue = self.text_value.text()

            if self.combox_select == "代理设置":
                self.dict_con.setdefault(self.combox_select, []).append(self.dictkey)
                msg = """<span style="color: rgba(255,134,0,1.00); padding-left: 12px; padding-right: 10px; 
                font-size: 11px;">%s</span></br>""" % str(self.dict_con)
                self.print_5.appendHtml(msg)
                self.print_5.appendHtml("-" * 50)
                self.print_1.append("%s->记录已添加" % self.combox_select)
                self.print_1.append("-" * 50)
            elif self.combox_select == "关键字表":
                self.dict_con.setdefault(self.combox_select, []).append(self.dictkey)
                msg = """<span style="color: rgba(255,134,0,1.00); padding-left: 12px; padding-right: 10px; 
                font-size: 11px;">%s</span></br>""" % str(self.dict_con)
                self.print_5.appendHtml(msg)
                self.print_5.appendHtml("-" * 50)
                self.print_1.append("%s->记录已添加" % self.combox_select)
                self.print_1.append("-" * 50)
            elif self.combox_select == "授权账号":
                self.dict_con.setdefault(self.combox_select, {}).update({self.dictkey: self.dictvalue})
                msg = """<span style="color: rgba(255,134,0,1.00); padding-left: 12px; padding-right: 10px; 
                font-size: 11px;">%s</span></br>""" % str(self.dict_con)
                self.print_5.appendHtml(msg)
                self.print_5.appendHtml("-" * 50)
                self.print_1.append("%s->记录已添加" % self.combox_select)
                self.print_1.append("-" * 50)
            else:
                self.dict_con.setdefault(self.combox_select, {}).update({self.dictkey: self.dictvalue})
                msg = """<span style="color: rgba(255,134,0,1.00); padding-left: 12px; padding-right: 10px; 
                font-size: 11px;">%s</span></br>""" % str(self.dict_con)
                self.print_5.appendHtml(msg)
                self.print_5.appendHtml("-" * 50)
                self.print_1.append("%s->记录已添加" % self.combox_select)
                self.print_1.append("-" * 50)
            self.text_key.clear()
            self.text_value.clear()
            self.save_config_click()
            self.check_file()
            self.but_save_config.setEnabled(True)
        else:
            pass

    # 双击删除 关键字 代理 下的item
    def Modify_dict(self):
        self.dialog.setWindowModality(Qt.ApplicationModal)
        self.dialog.setGeometry(500,400,150,191)
        dict_key = self.cmbox_revise.currentText()
        dict_key_list = self.dict_con.get(dict_key)
        if type(dict_key_list) == list:

            model = QStringListModel()
            for item in self.dict_con:
                if dict_key == item:
                    model.setStringList(self.dict_con[dict_key])
                    self.dialog.listView_dict.setModel(model)
                else:
                    pass
            self.dialog.show()
        else:
            msg = str([x for x, y in self.dict_con.get(dict_key).items()])
            msg = """<span style="color: rgba(255,162,29,1.00); padding-left: 10px; padding-right: 14px; 
                    font-size: 13px;">%s</span></br>""" % msg
            self.print_5.clear()
            self.print_5.appendHtml(msg)
            self.print_1.append("删除当前选择-【%s】频道，请点击旁边的删除频道"% dict_key)

    def save_config_click(self):
        with open('config.json', 'w', encoding="utf-8") as f:
            json.dump(self.dict_con, f, ensure_ascii=False)
        self.print_1.append("配置文件已经保存")
        self.print_1.append("-" * 50)

    def read_config(self):
        with open('config.json', 'r', encoding="utf-8") as f:
            self.dict_con = json.load(f)

            self.print_1.append("读取到【%s】个配置文件项目" % len(self.dict_con))
            # self.print_1.append(str(self.dict_con.keys())[10:-1])
            self.print_1.append("-" * 50)
            for item in self.dict_con:
                msg =("%s--->包含%s个项目" % (item,len(self.dict_con.get(item))))
                msg = """<span style="color: rgba(255,162,29,1.00); padding-left: 10px; padding-right: 12px;
                        font-size: 12px;">%s</span></br>""" % msg
                self.print_5.appendHtml(msg)
            self.print_5.appendHtml("-"*50)
            self.cmbox_revise.clear()
            self.cmbox_activation.clear()

    def del_dict(self):
        choose = QMessageBox.information(self, "重要提醒！！！", "确认删除", QMessageBox.Yes | QMessageBox.No)
        if choose == 16384:
            self.dict_con.clear()
            self.but_save_config.setEnabled(True)
            self.print_1.append("字典已经清空")
            self.print_1.append("-"*50)
            self.save_config_click()
        else:
            pass

    def del_keyworditem(self, item):
        self.dialog.close()
        key = self.cmbox_revise.currentText()
        dict_key_list = self.dict_con.get(key)
        if type(dict_key_list) == list:
            remind_box = QMessageBox.question(self, "删除项目", "是否删除选择的项目", QMessageBox.Yes | QMessageBox.No)

            if remind_box == 16384:
                if type(dict_key_list) != dict:
                    dict_key_list.remove(dict_key_list[item.row()])  # OK
                    model = QStringListModel()  # 重新设置数据来刷新
                    model.setStringList(dict_key_list)  # 重新设置数据来刷新
                    self.dialog.listView_dict.setModel(model)  # 重新设置数据来刷新
                    self.save_config_click()
                    self.check_file()
                    self.dialog.tableView_dict.setModel(model)
                else:
                    QMessageBox.information(self, "提示", "频道列表不能通过这种方式删除，关键字可以")

            else:

                pass
        else:
            self.print_1.append("删除当前选择-【%s】频道，请点击旁边的删除频道"% key)

    def del_key(self):
        choose = QMessageBox.information(self, "重要提醒！！！", "确认删除", QMessageBox.Yes | QMessageBox.No)
        if choose == 16384:
            delkey = self.cmbox_revise.currentText()
            self.dict_con.pop(delkey)
            self.save_config_click()
            self.check_file()
            print(self.dict_con)
        else:
            pass


    # -----------------------------------------------------------------系统按钮区
    def func_but_taici(self):
        import win32api
        win32api.ShellExecute(0, 'open', 'notepad.exe', "自定义台词.txt", '', 1)

    def func_but_daiban(self):
        import win32api
        win32api.ShellExecute(0, 'open', 'notepad.exe', "待办列表.txt", '', 1)

    def func_but_clear4(self):
        self.print_5.clear()

    def func_but_clear3(self):
        self.print_3.clear()
    # -----------------------------------------------------------------func_but_monitor2
    # -----------------------------------------------------------------func_but_monitor2
    def start2(self):
        if self.Thread_monitor2.isRunning():  # 如果该线程正在运行，则不再重新启动
            self.monitor2.exit_flag = True
            self.stop_thread2()
            self.but_monitor2.setText("监控[run]")
            return
        else:
            # 先启动QThread子线程
            self.func_but_monitor2()
            self.monitor2.exit_flag = False
            self.Thread_monitor2.start()
            # 发送信号，启动线程处理函数
            # 不能直接调用，否则会导致线程处理函数和主线程是在同一个线程，同样操作不了主界面
            self._startThread.emit()
            zz= self.cmbox_activation.currentText()
            self.but_monitor2.setText("监控[stop]")

    def stop_thread2(self):
        print("正在停止线程.....")
        if not self.Thread_monitor2.isRunning():
            return
        # self.Thread_monitor2.terminate()
        self.Thread_monitor2.quit()  # 退出
        self.Thread_monitor2.wait()  # 回收资源
        self.print_1.append("监控线程已经停止".center(50, "-"))
        print("监控线程已经停止")

    def func_but_monitor2(self):
        self.print_2.append(str(self.keyword_list))
        self.print_1.append("开始监控消息".center(50, "-"))
        self.active_args()
        # self.Thread_monitor2 = QThread(self)
        self.monitor2 = monitor_bot(self.ui_args)
        self.monitor2.moveToThread(self.Thread_monitor2)
        self._startThread.connect(self.monitor2.run)

        self.monitor2._sign_res1.connect(self.monitor2_callbake1)
        self.monitor2._sign_res2.connect(self.monitor2_callbake2)
        self.monitor2._sign_res3.connect(self.monitor2_callbake3)
        self.monitor2._sign_res4.connect(self.monitor2_callbake4)
        self.monitor2._sign_res5.connect(self.monitor2_callbake5)
        self.monitor2._sign_res6.connect(self.monitor2_callbake6)
        self.monitor2._sign_res7.connect(self.monitor2_callbake7)

        # self.Thread_monitor2.start()

        # 发送线程运行参数到ui

    # 不包含关键字
    def monitor2_callbake1(self, msg):
        msg = """<span style="font-size: 12px; color: rgb(116, 116, 236); 
        padding-right: 10px; padding-left: 5px;line-height: 100px;">%s</span>""" % msg
        self.print_5.appendHtml(msg)
        self.print_5.setStyleSheet("background-color:rgba(32,34,37,1.00);")

        pass

    def monitor2_callbake2(self, msg):
        msg = """<span style="color: rgba(162,162,162,1.00); padding-left: 13px; 
        padding-right: 15px; font-size: 15px;">%s</span></br>""" % msg
        self.print_5.appendHtml(msg)
        pass

    def monitor2_callbake3(self, msg):
        msg1 = """<style type="text/css">	
        a:link {color:rgba(79,79,79,1.00);text-decoration:none; margin-left: 20px;font-size: 13px}
        a:hover{color: rgba(79,79,79,1.00)}
        </style><a href="%s" >%s</a>""" % (msg, msg)
        self.print_5.appendHtml(msg1)
        msg2 = """<span style="font-size: 12px; color:rgba(79,79,79,1.00); padding-right: 11px; padding-left: 5px;">
        ------------------------------------------------------------------------------------</span>"""
        self.print_5.appendHtml(msg2)
        pass

    # 包含关键字
    def monitor2_callbake4(self, msg):
        msg = """<span style="font-size: 12px; color: rgb(116, 116, 236); padding-right: 10px; 
        padding-left: 5px;line-height: 100px;">%s</span>""" % msg
        self.print_3.appendHtml(msg)
        self.print_3.setStyleSheet("background-color:rgba(32,34,37,1.00);")

    def monitor2_callbake5(self, msg):
        msg = """<span style="color: rgba(255,162,29,1.00); padding-left: 10px; padding-right: 14px; 
        font-size: 13px;">%s</span></br>""" % msg
        self.print_3.appendHtml(msg)

    def monitor2_callbake6(self, msg):
        msg1 = """<style type="text/css">
        a:link {color:rgba(79,79,79,1.00);text-decoration:none; margin-top: 5px;font-size: 9px}
        a:hover{color: rgba(79,79,79,1.00)}
        </style><a href="%s" >%s</a>""" % (msg, msg)
        self.print_3.appendHtml(msg1)
        msg2 = """<span style="font-size: 11px; color:rgba(79,79,79,1.00); 
        padding-right: 9px; padding-left: 5px;">------------------------</span>"""
        self.print_3.appendHtml(msg2)
        pass

    # 发送状态
    def monitor2_callbake7(self, msg):
        self.print_4.append(str(msg))
        pass

    # -----------------------------------------------------------------func_but_monitor2
    # -----------------------------------------------------------------func_but_monitor
    def start(self):
        if self.Thread_monitor.isRunning():  # 如果该线程正在运行，则不再重新启动
            self.monitor.exit_flag = True
            self.stop_thread()
            self.but_monitor.setText("监控[run]")
            return
        else:
            # 先启动QThread子线程
            self.func_but_monitor()
            self.monitor.exit_flag = False
            self.Thread_monitor.start()
            # 发送信号，启动线程处理函数
            # 不能直接调用，否则会导致线程处理函数和主线程是在同一个线程，同样操作不了主界面
            self._startThread.emit()
            zz= self.cmbox_activation.currentText()
            self.but_monitor.setText("监控[stop]")

    def stop_thread(self):
        print("正在停止线程.....")
        if not self.Thread_monitor.isRunning():
            return
        # self.Thread_monitor.terminate()
        self.Thread_monitor.quit()  # 退出
        self.Thread_monitor.wait()  # 回收资源
        self.print_1.append("监控线程已经停止".center(50,"-"))
        print("监控线程已经停止")


    def func_but_monitor(self):
        self.print_2.append(str(self.keyword_list))
        self.print_1.append("开始监控消息".center(50,"-"))
        self.active_args()
        # self.Thread_monitor = QThread(self)
        self.monitor = monitor_bot(self.ui_args)
        self.monitor.moveToThread(self.Thread_monitor)
        self._startThread.connect(self.monitor.run)

        self.monitor._sign_res1.connect(self.monitor_callbake1)
        self.monitor._sign_res2.connect(self.monitor_callbake2)
        self.monitor._sign_res3.connect(self.monitor_callbake3)
        self.monitor._sign_res4.connect(self.monitor_callbake4)
        self.monitor._sign_res5.connect(self.monitor_callbake5)
        self.monitor._sign_res6.connect(self.monitor_callbake6)
        self.monitor._sign_res7.connect(self.monitor_callbake7)

        # self.Thread_monitor.start()

        # 发送线程运行参数到ui




    # 不包含关键字
    def monitor_callbake1(self, msg):
        msg = """<span style="font-size: 12px; color: rgb(116, 116, 236); 
        padding-right: 10px; padding-left: 5px;line-height: 100px;">%s</span>""" % msg
        self.print_5.appendHtml(msg)
        self.print_5.setStyleSheet("background-color:rgba(32,34,37,1.00);")

        pass

    def monitor_callbake2(self, msg):
        msg = """<span style="color: rgba(162,162,162,1.00); padding-left: 13px; 
        padding-right: 15px; font-size: 15px;">%s</span></br>""" % msg
        self.print_5.appendHtml(msg)
        pass

    def monitor_callbake3(self, msg):
        msg1 = """<style type="text/css">	
        a:link {color:rgba(79,79,79,1.00);text-decoration:none; margin-left: 20px;font-size: 13px}
        a:hover{color: rgba(79,79,79,1.00)}
        </style><a href="%s" >%s</a>""" % (msg, msg)
        self.print_5.appendHtml(msg1)
        msg2 = """<span style="font-size: 12px; color:rgba(79,79,79,1.00); padding-right: 11px; padding-left: 5px;">
        ------------------------------------------------------------------------------------</span>"""
        self.print_5.appendHtml(msg2)
        pass

    # 包含关键字
    def monitor_callbake4(self, msg):
        msg = """<span style="font-size: 12px; color: rgb(116, 116, 236); padding-right: 10px; 
        padding-left: 5px;line-height: 100px;">%s</span>""" % msg
        self.print_3.appendHtml(msg)
        self.print_3.setStyleSheet("background-color:rgba(32,34,37,1.00);")

    def monitor_callbake5(self, msg):
        msg = """<span style="color: rgba(255,162,29,1.00); padding-left: 10px; padding-right: 14px; 
        font-size: 13px;">%s</span></br>""" % msg
        self.print_3.appendHtml(msg)

    def monitor_callbake6(self, msg):
        msg1 = """<style type="text/css">
        a:link {color:rgba(79,79,79,1.00);text-decoration:none; margin-top: 5px;font-size: 9px}
        a:hover{color: rgba(79,79,79,1.00)}
        </style><a href="%s" >%s</a>""" % (msg, msg)
        self.print_3.appendHtml(msg1)
        msg2 = """<span style="font-size: 11px; color:rgba(79,79,79,1.00); 
        padding-right: 9px; padding-left: 5px;">------------------------</span>"""
        self.print_3.appendHtml(msg2)
        pass

    # 发送状态
    def monitor_callbake7(self, msg):
        self.print_4.append(str(msg))
        pass

    # -----------------------------------------------------------------func_but_monitor
    def func_but_sign(self):
        self.active_args()
        try:
            if self.Thread_sigin.isRunning() == True:
                self.Thread_sigin.quit()
                self.Thread_sigin.wait()
                self.Thread_sigin.deleteLater()
                print("线程正在运行")
            else:
                print("线程没有运行")

                self.print_1.append("线程没有运行")
        except:
            pass

        self.Thread_sigin = QThread()
        self.sigin = sigin_bot(self.ui_args)
        self.sigin.moveToThread(self.Thread_sigin)
        self.Thread_sigin.started.connect(self.sigin.run)

        self.sigin._sign_quit.connect(self.Thread_sigin.quit)
        self.sigin._sign_del.connect(self.Thread_sigin.deleteLater)
        self.sigin._sign_finished.connect(self.Thread_sigin.finished)

        self.sigin._sign_res1.connect(self.sigin_callbake1)
        self.sigin._sign_res2.connect(self.sigin_callbake2)

        self.Thread_sigin.start()
        pass

    def sigin_callbake1(self, msg):
        self.print_1.append(str(msg))

    def sigin_callbake2(self, msg):
        msg = """<span style="color: rgba(255,134,0,1.00); padding-left: 12px; padding-right: 10px; 
        font-size: 11px;">%s</span></br>""" % msg
        self.print_5.appendHtml(msg)

    # -----------------------------------------------------------------func_but_shortcut
    def func_but_shortcut(self):
        self.active_args()
        try:
            if self.Thread_reply.isRunning() == True:
                self.Thread_reply.quit()
                self.Thread_reply.wait()
                self.Thread_reply.deleteLater()

            else:
                print("线程没有运行")
                self.print_1.append("线程没有运行")
        except:
            pass
        self.Thread_reply = QThread()
        self.reply = reply_bot(self.ui_args)
        self.reply.moveToThread(self.Thread_reply)
        self.Thread_reply.started.connect(self.reply.run)

        self.reply._sign_quit.connect(self.Thread_reply.quit)
        self.reply._sign_del.connect(self.Thread_reply.deleteLater)
        self.reply._sign_finished.connect(self.Thread_reply.finished)

        self.reply._sign_res1.connect(self.reply_callbake1)
        self.reply._sign_res2.connect(self.reply_callbake2)
        self.reply._sign_res3.connect(self.reply_callbake3)

        self.Thread_reply.start()
        self.input_shortcut.clear()
        self.print_1.append("---等待结果返回---")
        pass

    def reply_callbake1(self, msg):

        self.print_1.append(str(msg))

    def reply_callbake2(self, msg):
        self.print_1.append(str(msg))

        pass

    def reply_callbake3(self, msg):
        self.print_1.append(msg)

        pass

    # -----------------------------------------------------------------func_but_shortcut
    # -----------------------------------------------------------------doublecha_bot
    def start_doublecha(self):
        if len(self.auths_list) <2:
            print("交互模式最少2个账号")
            self.print_1.append("交互模式最少2个账号".center(50,"-"))
        else:
            if self.Thread_doublecha.isRunning():  # 如果该线程正在运行，则不再重新启动
                self.doublecha.exit_flag3 = True
                self.stop_thread_doublecha()
                self.but_double_cha.setText("交互[run]")
                return
            else:
                # 先启动QThread子线程
                self.func_doublecha()
                self.doublecha.exit_flag3 = False
                self.Thread_doublecha.start()
                # 发送信号，启动线程处理函数
                # 不能直接调用，否则会导致线程处理函数和主线程是在同一个线程，同样操作不了主界面
                self._startThread3.emit()
                self.but_double_cha.setText("交互[stop]")

    def stop_thread_doublecha(self):
        print("正在停止线程.....")
        if not self.Thread_doublecha.isRunning():
            return
        # self.Thread_monitor.terminate()
        self.Thread_doublecha.quit()  # 退出
        self.Thread_doublecha.wait()  # 回收资源
        print("交互线程已经停止")


    def func_doublecha(self):
        self.print_1.append("交互模式开始发送消息".center(50, "-"))
        self.active_args()

        self.doublecha = doublecha_bot(self.ui_args)
        self.doublecha.moveToThread(self.Thread_doublecha)
        self.Thread_doublecha.started.connect(self.doublecha.run)

        self.doublecha._sign_res1.connect(self.doublecha_callbake1)
        self.doublecha._sign_res2.connect(self.doublecha_callbake2)

        # self.Thread_doublecha.start()
        pass

    def doublecha_callbake1(self, msg):
        self.print_2.append(str(msg))


    def doublecha_callbake2(self, msg):
        self.print_1.append(str(msg))
        pass




    # -----------------------------------------------------------------doublecha_bot
    # -----------------------------------------------------------------func_but_sendmessage
    def start_send(self):
        if self.Thread_send.isRunning():  # 如果该线程正在运行，则不再重新启动
            self.send.exit_flag2 = True
            self.stop_thread_send()
            self.but_send.setText("群发[run]")
            return
        else:
            # 先启动QThread子线程
            self.func_but_send()
            self.send.exit_flag2 = False
            self.Thread_send.start()
            # 发送信号，启动线程处理函数
            # 不能直接调用，否则会导致线程处理函数和主线程是在同一个线程，同样操作不了主界面
            self._startThread2.emit()
            self.but_send.setText("群发[stop]")

    def stop_thread_send(self):
        print("正在停止线程.....")
        if not self.Thread_send.isRunning():
            return
        # self.Thread_monitor.terminate()
        self.Thread_send.quit()  # 退出
        self.Thread_send.wait()  # 回收资源
        print("线程已经停止")

    def func_but_send(self):
        self.print_1.append("开始发送消息".center(50,"-"))
        self.active_args()

        self.send = send_bot(self.ui_args)
        self.send.moveToThread(self.Thread_send)
        self._startThread2.connect(self.send.run)

        self.send._sign_res1.connect(self.send_callbake1)
        self.send._sign_res2.connect(self.send_callbake2)

        # self.Thread_send.start()
        pass

    def send_callbake1(self, msg):
        self.print_2.append(str(msg))#[2:-2]


    def send_callbake2(self, msg):
        self.print_1.append(str(msg))

    # -----------------------------------------------------------------func_but_sendmessage

    def _exit(self):
        app.close()
        print("退出程序")
        sys.exit()

    # -----------------------------------------------------------------


if __name__ == "__main__":
    App = QApplication(sys.argv)
    app = BoxMain()
    app.show()
    sys.exit(App.exec())
