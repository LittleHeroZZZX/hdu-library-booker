from ast import arg
from sched import scheduler
from urllib import response
from pytz import timezone
import requests as req
import datetime as dt
import time
from time import sleep
import yaml
import os
import argparse
from pprint import pp, pprint
import logging
from tqdm import tqdm
import sys
import signal
import pandas as pd
from apscheduler.schedulers.blocking import BlockingScheduler
req.packages.urllib3.disable_warnings()


pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)
pd.set_option('display.width', None)
pd.set_option("display.colheader_justify", "center")

class Library():
    def __init__(self, config_file = None) -> None:
        self.config_file = config_file
        self.load_config(config_file)
    
    def load_config(self, config_file):
        """
        加载配置文件
        """
        if not os.path.exists(config_file):
            raise FileNotFoundError("config file not found")
        if not config_file.endswith(".yaml") and not config_file.endswith(".yml"):
            raise ValueError("config file must be a yaml file")
        with open(config_file, "r", encoding="utf-8") as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
        try:
            self.config = config
            self.user_info = config["user_info"].copy()
            self.session_config = config["session"]
            self.session = req.Session()
            self.session.trust_env = self.session_config["trust_env"]
            self.session.headers = self.session_config["headers"]
            self.session.params = self.session_config["params"]
            self.session.verify = self.session_config["verify"]
            self.urls = self.session_config["urls"]
            self.seat_list = config["seat_list"]
            self.data = config["data"]
            self.settings = config["settings"]
            
        except KeyError as e:
            raise KeyError(e)
    
    def update_config(self):
        """
        更新配置文件
        """
        # self.config["user_info"] = self.user_info
        self.config["session"] = self.session_config
        self.config["seat_list"] = self.seat_list
        self.config["data"] = self.data
        self.config["settings"] = self.settings
        self.save_config(self.config_file)

    def save_config(self, config_file):
        """
        保存配置文件
        """
        with open(config_file, "w+", encoding="utf-8") as f:
            yaml.dump(self.config, f)

    def set_username_and_password(self):
        """
        设置用户名和密码
        """
        self.user_info["login_name"] = input("请输入学号：")
        self.user_info["password"] = input("请输入密码：")
        self.user_info["org_id"] = "104"

    def login(self):
        """
        登录
        """
        if self.user_info["login_name"] == "" or self.user_info["password"] == "" or self.user_info["login_name"] is None or self.user_info["login_name"] is None:
            print("配置文件中学号或密码为空，请重新输入")
            self.set_username_and_password()
        url = self.urls["login"]
        login_res = self.session.post(url=url, data=self.user_info).json()
        if login_res["CODE"] == "ok":
            if self.user_info != self.config["user_info"]:
                if input("是否需要保存密码至配置文件，若保存下次可自动登录(y/n)") == "y":
                    self.config["user_info"] = self.user_info
                    self.save_config(self.config_file)
                    print("保存成功！")
            return True
        else:
            print("登录失败，请重新输入账号密码")
            self.set_username_and_password()
            self.login()
            return True

    def _query_seats(self, data):
        """
        查询指定时间段的座位
        """
        url = self.urls["query_seats"]
        try:
            res = self.session.post(url, data=data, verify=False).json()["allContent"]["children"][2]["children"]["children"]
        except KeyError:
            return []
        return res

    def query_and_add_seat(self):
        """
        添加待抢座位列表
        seatinfo字段为：
            data: 查询座位信息需要post的data
                字段为：
                    beginTime: 开始日期
                    duration: 预约时长
                    num: 预约座位数
                    space_category[category_id]: "591" 未知
                    space_category[content_id]: "3"/"76" 图书馆/自习室
            begin_time: 预约开始时间
            duration: 预约时长
            end_time: 预约结束时间
            status: 座位状态
                0:"空座位"
                1:"已被选"
                3:"被ban"

        """
        seat_info = {}
        time = input("请输入预约开始时间（格式：yyyy-mm-dd hh:mm:ss，如 2022-01-01 13:01:00）,输入0表示当前时间\n")
        if time == "0":
            time = dt.datetime.now().timestamp()
        else:
            try:
                time = dt.datetime.strptime(time, "%Y-%m-%d %H:%M:%S").timestamp()
            except:
                print("时间格式错误！")
                return
        print("请输入预约时长（单位：小时，整数）")
        print("**请自行保证设置的预约开始时间和预约时间是合理的，本脚本将不对其校验。错误的时间将导致无法预约，甚至有封号的风险！**")
        duration = int(input("请输入预约时长（单位：小时，整数）"))*3600
        query_data = self.data["query_data"].copy()
        query_data.update({
            "beginTime": str(time),
            "duration": str(duration)
        })
        content_id = input("请输入预约类型（3：自习室，76：阅览室）")
        query_data["space_category[content_id]"] = content_id
        query_res = self._query_seats(query_data)
        room_names = [x["roomName"] for x in query_res]
        print("查询到的楼层为：")
        for i, room_name in enumerate(room_names):
            print(str(i+1)+"\t"+room_name)
        room_id = int(input("请输入座位楼层的编号："))
        room_name = room_names[room_id-1]
        seat_title = input("请输入座位编号：")
        try:
            seat = [ x   for x in query_res[room_id-1]["seatMap"]["POIs"] if x["title"]==seat_title][0]
        except:
            print("不存在该座位！")
            print("请重新添加待选座位！")
            self.query_and_add_seat()
            return
        seat_id = seat["id"]
        booker = query_res[0]["userInfo"]["id"]
        if seat["state"] == "3":
            # ban位
            print("该座位为ban位，不可预约！")
            print("是否需要强行加入预约列表（强烈不推荐）？(y/n)")
            if input() != "y":
                print("请重新添加待选座位！")
                self.query_and_add_seat()
                return
        
        begin_time = dt.datetime.fromtimestamp(time)
        end_time = begin_time + dt.timedelta(seconds=duration)

        status_dict = {
            "0":"空座位",
            "1":"已被选",
            "3":"被ban"
        } 
        book_data = {
            "beginTime": str(time),
            "duration": str(duration),
            "seats[0]": seat_id,
            "seatBookers[0]": booker
        }

        seat_info["位置"] = f"{room_name}-{seat_title}"
        seat_info["状态"] = status_dict[str(seat["state"])]
        seat_info["data"] = book_data
        seat_info["开始时间"] = begin_time.strftime("%Y-%m-%d %H:%M:%S")
        seat_info["持续时间"] = str(duration/3600)+"小时"
        seat_info["结束时间"] = end_time.strftime("%Y-%m-%d %H:%M:%S")
        self.seat_list.append(seat_info)
        print("添加成功！")
        print("是否继续添加待选座位？(y/n)")
        if input() == "y":
            self.query_and_add_seat()
        
        return

    def show_seat_list(self):
        """
        显示待选座位列表，并执行添加或删除操作
        """
        if len(self.seat_list) == 0:
            print("暂无待选座位！")
            print("请先添加座位！")
            self.query_and_add_seat()
            return
        print("当前待选座位列表：")
        # for i, seat in enumerate(self.seat_list):
        #     print("-"*100)
        #     seat_temp = seat.copy()
        #     seat_temp.pop("data")
        #     pprint({f"序号{i+1}":seat_temp})
        df_seats = pd.DataFrame(self.seat_list)
        df_seats.drop("data", axis=1, inplace=True)
        df_seats.loc[:, "序号"] = df_seats.index
        temp_df = df_seats["位置"].str.split("-", expand=True)
        df_seats["楼层"] = temp_df[0]
        df_seats["座位"] = temp_df[1]
        df_seats.drop(["位置"], axis=1, inplace=True)
        df_seats = df_seats.loc[:,["序号","楼层","座位","状态","开始时间","结束时间", "持续时间"]]
        df_seats.index = df_seats["序号"]
        df_seats.drop(["序号"], axis=1, inplace=True)
        df_seats.index.name = None
        df_seats.columns.name = "序号"
        # df_seats.style.set_properties(**{'text-align': 'center'})  error: Backend Qt5Agg is interactive backend. Turning interactive mode on.
        print(df_seats)
        print("="*100)
        op = input("请输入需要删除的座位序号，以英文逗号分割，输入0表示不删除，输入-1表示删除所有座位\n")
        if op == "-1":
            self.seat_list = []
            return
        if op == "0":
            pass
        else:
            try:
                del_list = [int(x)-1 for x in input().split(",")]
                self.seat_list = [seat for i, seat in enumerate(self.seat_list) if i not in del_list]
            except:
                print("输入错误！")
                self.show_seat_list()
        if input("是否继续添加待选座位？(y/n)") == "y":
            self.query_and_add_seat()

        
        


    def run(self):
        """
        按seatlist列表顺序抢座位
        """
        global show_log
        interval = self.settings["interval"]
        max_try_times = self.settings["max_try_times"]
        print(f"当前抢座位时间间隔为：{interval}秒，最大尝试次数为：{max_try_times}")
        print("开始抢座位！")
        for _ in tqdm(range(max_try_times), file=sys.stdout):
            for seat in self.seat_list:
                data = seat["data"]
                url = self.urls["book_seat"]
                response = self.session.post(url, data=data).json()
                if response["CODE"] == "ok":
                    print("预约成功！作为详细信息如下：")
                    print(f"座位：{seat['location']}")
                    print(f"开始时间：{seat['begin_time']}")
                    print(f"结束时间：{seat['end_time']}")
                    print(f"预约时长：{seat['duration']}小时")
                    return True
                else:
                    if show_log:
                        print(response)
                    sleep(interval)
        print("抢座位失败！")
    def update_seat_time(self):
        """
        将作为列表中的时间更新为指定时间
        """
        begin_time = input("请输入开始时间（格式：yyyy-mm-dd hh:mm:ss）：")
        duration = int(input("请输入预约时长（单位：小时）："))*3600
        begin_time = dt.datetime.strptime(begin_time, "%Y-%m-%d %H:%M:%S")
        for seat in self.seat_list:
            seat["开始时间"] = dt.datetime.strftime(begin_time, "%Y-%m-%d %H:%M:%S")
            seat["持续时间"] = str(duration/3600)+"小时"
            seat["结束时间"] = dt.datetime.strftime(begin_time + dt.timedelta(seconds=duration), "%Y-%m-%d %H:%M:%S")
            seat["data"]["beginTime"] = begin_time.timestamp()
            seat["data"]["duration"] = duration
        print("更新成功！")
        sleep(1)

    def specify_time(self):
        """
        指定时间抢座位
        """
        time = input("请输入程序开始运行时间（格式：yyyy-mm-dd hh:mm:ss）：")
        time = dt.datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
        time_now = dt.datetime.now()
        time_delta = time - time_now
        if time_delta.total_seconds() < 0:
            print("指定时间已过！")
            sleep(1)
            return
        elif time_delta.total_seconds() > 24*3600:
            print("指定时间超过一天！请明天再运行本程序！")
            sleep(1)
            return
        else:
            hours, minutes, seconds = time_delta.seconds//3600, time_delta.seconds//60%60, time_delta.seconds%60
            print(f"程序将在{hours}小时{minutes}分钟{seconds}秒后开始运行！")
            print("请保持程序运行，程序将在指定时间后自动抢座！")
            scheduler = BlockingScheduler(timezone="Asia/Shanghai")
            scheduler.add_job(self.run, "cron", year=time.year, month=time.month, day=time.day, hour=time.hour, minute=time.minute, second=time.second)
            scheduler.start()



                    


    


if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", help="config file path", type=str, default="config.yaml")
    parser.add_argument("-l", "--show_log", help="show log", type=bool, default=True)
    args = parser.parse_args()
    global show_log 
    show_log = args.show_log
    try:
        lib = Library(args.config)
    except KeyError as e:
        print(f"配置文件{args.config}中缺少键值{e}，请检查配置文件，程序将退出...")
        exit(1)
    except FileNotFoundError as e:
        print(f"指定配置文件不存在，请确认文件存在{args.config}（默认配置文件为config.yaml）")
        print("程序将退出...")
        exit(1)
    except ValueError as e:
        print(f"配置文件必须为.yaml或.yml格式，请检查配置文件，程序将退出...")
        exit(1)
    print("配置文件加载成功！")
    try:
        lib.login()
    except Exception as e:
        print(f"发生异常！")
        print(e)
        exit(1)
    print("登录成功！")
    print("="*100)
    print("欢迎使用抢座位小工具！")
    print("本工具将自动保存上次待抢座位列表，使用前请先查看待选座位列表")
    while 1:
        print("="*100)
        print("\n\n")
        print("""请输入功能代码：
            1、 修改待选座位列表
            2、 一键更新待抢座位时间（批量修改列表中的预约时间段）
            3、 开始抢座位
            4、 定时抢座位
            5、 退出
            """)
        fun = input()
        lib.update_config()
        if fun == "1":
            lib.show_seat_list()
        elif fun == "3":
            lib.run()
        elif fun == "2":
            lib.update_seat_time()
        elif fun == "4":
            lib.specify_time()
        else:
            lib.update_config()
            print("程序退出！")
            exit(0)


    
    
    

    
    