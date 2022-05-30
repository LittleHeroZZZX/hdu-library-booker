from turtle import update
from webbrowser import get
from PySide2 import QtCore, QtGui, QtWidgets, QtUiTools
import sys
from PySide2.QtWidgets import QApplication
from pyrsistent import b
from hduBooker import Hdubooker
from PySide2.QtCore import Qt
from PandasModel import PandasModel
import types
import time
import threading
QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)

class Mysignal(QtCore.QObject):
    mysignal = QtCore.Signal(dict)



class UI():
    def __init__(self):
        self.help = {
            "login":"欢迎使用hdu-booker！\n请输入图书馆账号密码进行登录！",
            "main":"首次使用请先点击\"修改座位列表\"添加待抢座位列表。\n座位添加完毕后，点击\"立即开始抢座\"开始抢座，也可设置开始抢座时间在指定时间开始抢座！请勿随意修改请求间隔，频率过高有封号风险！\n提示：通常自习室座位放出时间为晚八点，书库座位放出时间为晚九点！\n",
            "change":"在左上角按提示可添待选座位\n点击\"统一修改时间\"可以将待抢座列表所有时间改为指定时间\n选择某条记录后点击\"删除制定项\"可删除该条记录"
        }
        self.loader = QtUiTools.QUiLoader()
        self.init_booker()
        self.load_login_ui()
        self.show_login_ui()
    
    def init_booker(self):
        """
        初始化hdubooker类，加载配置文件，若配置文件不存在，则退出程序
        """
        try:
            self.booker = Hdubooker("config/config.yaml")
        except FileNotFoundError as e:
            box = QtWidgets.QMessageBox(self.login_ui)
            box.setText("未找到指定配置文件！\n请检查程序运行目录下是否存在config.yaml文件！")
            quitButton = box.addButton("退出", QtWidgets.QMessageBox.YesRole)
            box.setWindowTitle("错误")
            box.exec_()
            if box.clickedButton() == quitButton:
                sys.exit(0)
        except ValueError as e:
            box = QtWidgets.QMessageBox(self.login_ui)
            box.setText("配置文件必须为yaml文件！")
            quitButton = box.addButton("退出", QtWidgets.QMessageBox.YesRole)
            box.setWindowTitle("错误")
            box.exec_()
            if box.clickedButton() == quitButton:
                sys.exit(0)
        except KeyError as e:
            box = QtWidgets.QMessageBox(self.login_ui)
            box.setText("配置文件中缺少必要的配置项！")
            quitButton = box.addButton("退出", QtWidgets.QMessageBox.YesRole)
            box.setWindowTitle("错误")
            box.exec_()
            if box.clickedButton() == quitButton:
                sys.exit(0)


    def load_login_ui(self):
        self.login_ui = self.loader.load('./ui/login.ui')
        self.login_ui.login_button.clicked.connect(self.login)
        self.login_ui.setWindowIcon(QtGui.QIcon("./icon.ico"))
         

    def show_login_ui(self):
        if self.booker.user_info["login_name"]  and self.booker.user_info["password"]:
            self.login_ui.username.setText(self.booker.user_info["login_name"])
            self.login_ui.password.setText(self.booker.user_info["password"])
        self.login_ui.show()
        QtWidgets.QMessageBox.information(self.login_ui, "帮助", self.help["login"])

    def load_main_ui(self):
        self.main_ui = self.loader.load('./ui/main.ui')
        self.main_ui.setWindowIcon(QtGui.QIcon("./icon.ico"))
        self.main_ui.change_button.clicked.connect(self.show_change_ui)
        self.main_ui.imme_run_button.clicked.connect(self.run_imme)
        self.main_ui.wait_run_button.clicked.connect(self.run_wait)
        user_info = self.booker.user_info
        time = QtCore.QDateTime.currentDateTime()
        self.main_ui.begin_date.setDate(time.date())
        self.main_ui.begin_time.setTime(time.time())
        self.main_ui.status.setText("未运行")
        if time.time().hour() < 12:
            greeting = "早上好"
        elif time.time().hour() < 18:
            greeting = "下午好"
        else:
            greeting = "晚上好"
        self.main_ui.user_info.setText(f"{user_info['name']}，{greeting}！欢迎使用hdu-booker！")
        self.main_ui.interval.setText("5")
        self.main_ui.max_try_times.setText("100")
        self.show_main_ui()
        QtWidgets.QMessageBox.information(self.main_ui, "帮助", self.help["main"])
    
    def load_change_ui(self):
        self.change_ui = self.loader.load('./ui/change.ui')
        self.change_ui.setWindowIcon(QtGui.QIcon("./icon.ico"))
        self.change_ui.add_button.clicked.connect(self.add_seat)
        self.change_ui.delete_all_button.clicked.connect(self.delete_all)
        self.change_ui.delete_one_button.clicked.connect(self.delete_one)
        self.change_ui.uniform_change_button.clicked.connect(self.uniform_change)
        self.update_seat_table(self.change_ui.seat_table)
        # fun_type = type(self.change_ui.closeEvent)
        # self.change_ui.closeEvent = fun_type(self.closeEvent,self.change_ui,QtWidgets.QWidget)
        
    
    
    def show_change_ui(self):
        # 日期和时间默认显示为当前时间
        self.load_change_ui()
        self.change_ui.begin_date.setDate(QtCore.QDate.currentDate())
        self.change_ui.begin_time.setTime(QtCore.QTime.currentTime())
        self.change_ui.uniform_begin_date.setDate(QtCore.QDate.currentDate())
        self.change_ui.uniform_begin_time.setTime(QtCore.QTime.currentTime())
        self.update_floor_list(self.change_ui.floor)
        self.change_ui.show()
        QtWidgets.QMessageBox.information(self.change_ui, "帮助", self.help["change"])

    def show_main_ui(self):
        self.update_seat_table(self.main_ui.seat_table)
        self.main_ui.show()
    
    

    def uniform_change(self):
        date = self.change_ui.uniform_begin_date.date()
        time = self.change_ui.uniform_begin_time.time()
        begin_time = QtCore.QDateTime(date, time).toTime_t()
        duration = self.change_ui.uniform_duration.time()
        duration = duration.hour() * 3600 + duration.minute() * 60 + duration.second()
        self.booker.uniform_change(begin_time, duration)
        self.update_seat_table(self.change_ui.seat_table)
        QtWidgets.QMessageBox.information(self.change_ui, "提示", "更改成功！")
        self.update_config()



    def delete_all(self):
        QtWidgets.QMessageBox.warning(self.change_ui, "警告", "确定要删除所有座位信息吗？", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
        if QtWidgets.QMessageBox.Yes == QtWidgets.QMessageBox.Yes:
            self.booker.delete_all()
            self.update_config()
            self.update_seat_table(self.change_ui.seat_table)
            self.update_seat_table(self.main_ui.seat_table)
            # self.update_floor_list(self.change_ui.floor)
            self.change_ui.seat_table.setCurrentIndex(self.change_ui.seat_table.model().index(0, 0))
    
    def run_imme(self):
        run_finished = Mysignal()
        run_finished.mysignal.connect(self.show_res)
        th = threading.Thread(target=self._run_imme, args=(run_finished,))
        th.start()

    def show_res(self, res):
        if res["status"]:
            seat = res["seat_info"]

            QtWidgets.QMessageBox.information(self.main_ui, "抢座成功","楼层：{}\n座位：{}\n开始时间：{}\n结束时间:{}".format(seat["floor"], seat["seat_number"], seat["begin_time"], seat["end_time"]))
            self.main_ui.status.setText("抢座成功")
            self.main_ui.status.setStyleSheet("color:green")
        else:
            QtWidgets.QMessageBox.warning(self.main_ui, "抢座失败","达到最大抢座次数，抢座失败！" )
            self.main_ui.status.setText("抢座失败")
            self.main_ui.status.setStyleSheet("color:red")
        self.main_ui.imme_run_button.setEnabled(True)
        self.main_ui.wait_run_button.setEnabled(True)
        self.main_ui.change_button.setEnabled(True)

    def run_wait(self):
        run_finished = Mysignal()
        run_finished.mysignal.connect(self.show_res)
        
        date = self.main_ui.begin_date.date()
        time = self.main_ui.begin_time.time()
        begin_time = QtCore.QDateTime(date, time)

        time_now = QtCore.QDateTime.currentDateTime()
        wait_secs = time_now.secsTo(begin_time)-time.second()
        if wait_secs < 0:
            th = threading.Thread(target=self._run_imme, args=(run_finished,))
            th.start()
        else:
            th = threading.Thread(target=self._run_imme, args=(run_finished, wait_secs))
            th.start()
        try:
            self.change_ui.close()
        except:
            pass
        self.main_ui.imme_run_button.setEnabled(False)
        self.main_ui.wait_run_button.setEnabled(False)
        self.main_ui.change_button.setEnabled(False)
        self.main_ui.status.setText("等待中")
            

    def _run_imme(self, run_finished, sleep_time = 0):
        print(sleep_time)
        time.sleep(sleep_time)
        self.booker.settings["interval"] = int(self.main_ui.interval.text())
        self.booker.settings["max_try_times"] = int(self.main_ui.max_try_times.text())
        self.update_config()
        
        
        self.main_ui.status.setText("运行中")
        self.main_ui.status.setStyleSheet("color:red")
        self.main_ui.imme_run_button.setEnabled(False)
        self.main_ui.wait_run_button.setEnabled(False)
        self.main_ui.change_button.setEnabled(False)
        try:
            self.change_ui.close()
        except:
            pass
        res = self.booker.run()
        run_finished.mysignal.emit(res)
        
    
        
    
    

        


    def delete_one(self):
        self.booker.delete_one(self.change_ui.seat_table.currentIndex().row())
        self.update_config()
        self.update_seat_table(self.change_ui.seat_table)
        self.update_seat_table(self.main_ui.seat_table)
        self.update_floor_list(self.change_ui.floor)
        self.change_ui.seat_table.setCurrentIndex(self.change_ui.seat_table.model().index(0, 0))
        self.update_config()

    def update_seat_table(self, seat_table):
        seat_list = self.booker.get_seat_list()
        model = PandasModel(seat_list)
        seat_table.setModel(model)
        seat_table.setColumnWidth(0, 150)
        seat_table.setColumnWidth(3, 150)
        seat_table.setColumnWidth(4, 150)

    def update_floor_list(self, floor):
        """
        维护楼层选项下拉框
        """
        floors = self.booker.get_floor_list()
        floors.reverse()
        floor.clear()
        for f in floors:
            floor.addItem(f)
        floor.setCurrentIndex(0)


    def check_seatinfo_valid(self):
        # todo 检查输入的座位信息是否合法
        seat_info = self.get_input_seatinfo()
        res = self.booker.check_seat_exist(seat_info)
        if res["status"]:
            QtWidgets.QMessageBox.information(self.change_ui, "提示", "座位信息合法！")
            self.change_ui.add_button.setEnabled(True)
        else:
            QtWidgets.QMessageBox.warning(self.change_ui, "提示", res["message"])
            self.change_ui.add_button.setEnabled(False)

    def add_seat(self):
        seat_info = self.get_input_seatinfo()
        res = self.booker.add_seat(seat_info)
        if res["status"]:
            self.update_seat_table(self.change_ui.seat_table)
            self.update_seat_table(self.main_ui.seat_table)
            self.update_config()
            QtWidgets.QMessageBox.information(self.change_ui, "提示", "添加座位成功！")
            
        else:
            QtWidgets.QMessageBox.warning(self.change_ui, "提示", res["message"])

    def update_config(self):
        self.booker.update_config()


    def get_input_seatinfo(self):
        """
        获取输入作为的信息，返回一个seatinfo字典
        seatinfo字段为：
             data: 查询座位信息需要post的data
                字段为：
                    "beginTime": 开始时间,
                    "duration": 持续时间（秒）,
                    "seats[0]": 座位号,
                    "seatBookers[0]": 预订人id
            floor: 楼层
            seat_number: 座位号
            begin_time: 预约开始时间
            duration: 预约时长
            end_time: 预约结束时间
            status: 座位状态（是否被ban）
                0:"空座位"
                1:"已被选"
                3:"被ban"
        """
        seatinfo = {}
        floor = self.change_ui.floor.currentText()
        seat_number = self.change_ui.seat_number.text()
        seatinfo["floor"] = floor
        seatinfo["seat_number"] = seat_number
        seatinfo["data"] = {}
        time = self.change_ui.begin_time.time()
        date = self.change_ui.begin_date.date()
        begin_time = QtCore.QDateTime(date, time)
        seatinfo["begin_time"] = begin_time.toString("yyyy-MM-dd hh:mm:ss")
        duration = self.change_ui.duration.time()
        seatinfo["duration"] = str(duration.hour() * 3600 + duration.minute() * 60 + duration.second())
        end_time = begin_time.addSecs(duration.hour() * 3600 + duration.minute() * 60 + duration.second())
        seatinfo["end_time"] = end_time.toString("yyyy-MM-dd hh:mm:ss")
        seatinfo["data"]["beginTime"] = str(begin_time.toTime_t())
        seatinfo["data"]["duration"] = str(duration)
        seatinfo["data"]["seats[0]"] = seat_number
        seatinfo["data"]["seatBookers[0]"] = self.booker.user_info["id"]
        return seatinfo

    def login(self):
        username = self.login_ui.username.text()
        password = self.login_ui.password.text()
        self.booker.set_username_and_password(username, password)
        if self.booker.login() is False:
            box = QtWidgets.QMessageBox(self.login_ui)
            box.setText("登录失败！\n学号或密码错误！")
            quitButton = box.addButton("确定", QtWidgets.QMessageBox.YesRole)
            box.setWindowTitle("错误")
            box.exec_()
        else:
            box = QtWidgets.QMessageBox(self.login_ui)
            box.setText("登录成功！")
            quitButton = box.addButton("确定", QtWidgets.QMessageBox.YesRole)
            box.setWindowTitle("成功！")
            box.exec_()
            self.login_ui.hide()
            
            self.load_main_ui()


if __name__=="__main__":
    app = QtWidgets.QApplication()
    hdubooker = UI()
    sys.exit(app.exec_())