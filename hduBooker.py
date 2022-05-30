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


class Hdubooker():
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
    def login(self):
        """
        登录
        """
        url = self.urls["login"]
        login_res = self.session.post(url=url, data=self.user_info).json()
        if login_res["CODE"] == "ok":
            self.init_user_info()
            return True
        else:
            return False
        
    def init_user_info(self):
        """
        初始化用户信息
        """
        user_info = self._query_seats()[0]["userInfo"]
        self.user_info["name"] = user_info["name"]
        self.user_info["id"] = user_info["id"]



    def set_username_and_password(self, username, password):
        """
        设置用户名和密码
        """
        self.user_info["login_name"] = username
        self.user_info["password"] = password

    def get_seat_list(self):
        """
        获取座位列表
        """
        df_seats = pd.DataFrame(self.seat_list)
        if not df_seats.empty:
            df_seats.drop("data", axis=1, inplace=True)
            df_seats.drop("duration", axis=1, inplace=True)
            df_seats = df_seats.loc[:,["floor","seat_number","status","begin_time","end_time"]]
            df_seats.columns=["楼层","座位号","是否被ban","开始时间","结束时间"]
            df_seats.index.name = None
            df_seats.columns.name = "序号"
        return df_seats
    
    def get_floor_list(self):
        """
        获取楼层列表
        """
        seats = self._query_seats()
        floor = [x["roomName"] for x in seats]
        return floor


    def _query_seats(self, data=None):
        """
        查询指定时间段的座位
            data: 查询座位信息需要post的data
            字段为：
                beginTime: 开始日期
                duration: 预约时长
                num: 预约座位数
                space_category[category_id]: "591" 未知
                space_category[content_id]: "3"/"76" 图书馆/自习室
            
        """
        if data is None:
            data={} #查询座位信息需要post的data
            today = dt.date.today()+dt.timedelta(days=3)
            begin_time = dt.datetime.combine(today, dt.time(10, 0, 0)).timestamp()
            duration = 3600
            num = 1
            data["beginTime"] = str(begin_time)
            data["duration"] = str(duration)
            data["num"] = str(num)
        data["space_category[category_id]"] = "591"
        data1 = data.copy()
        data2 = data.copy()
        data1["space_category[content_id]"] = "3"
        data2["space_category[content_id]"] = "76"


        url = self.urls["query_seats"]
        try:
            res1 = self.session.post(url, data=data1, verify=False).json()["allContent"]["children"][2]["children"]["children"]
            res2 = self.session.post(url, data=data2, verify=False).json()["allContent"]["children"][2]["children"]["children"]
            res = res1+res2
        except KeyError:
            return []
        return res

    def uniform_change(self, begin_time, duration):
        """
        统一改变座位预约时间
        """
        begin_time = dt.datetime.fromtimestamp(begin_time)
        end_time = begin_time + dt.timedelta(seconds=duration)
        for seat in self.seat_list:
            
            seat["begin_time"] = begin_time.strftime("%Y-%m-%d %H:%M:%S")
            seat["end_time"] = end_time.strftime("%Y-%m-%d %H:%M:%S")
            seat["duration"] = duration
            seat["data"]["beginTime"] = str(begin_time.timestamp())
            seat["data"]["duration"] = str(duration)


    def delete_all(self):
        """
        删除所有预约
        """
        self.seat_list = []
    
    def delete_one(self, index):
        """
        删除指定座位的预约
        """
        self.seat_list.pop(index)

    def add_seat(self, seatinfo):
        """
        首先检查检查座位号在该楼层是否存在
        若存在，则添加座位信息
        seatinfo字段为：
            data: 查询座位信息需要post的data
                字段为：
                    "beginTime": 开始时间,
                    "duration": 持续时间（秒）,
                    "seats[0]": 唯一座位号（与座位号不一致，为内部标识号）,
                    "seatBookers[0]": 预订人id
            floor: 楼层（必须）
            seat_number: 座位号（必须）
            begin_time: 预约开始时间（必须）
            duration: 预约时长（必须）
            end_time: 预约结束时间（必须）
            status: 座位状态（是否被ban）
                0:"空座位"
                1:"已被选"
                3:"被ban"
        """
        res = {"status": None, "message": None}
        query_res = self._query_seats()
        floors = [x["roomName"] for x in query_res]
        if seatinfo["floor"] not in floors:
            res["status"] = False
            res["message"] = "楼层不存在"
            return res
        for res in query_res:
            if res["roomName"] == seatinfo["floor"]:
                seat = [ x   for x in res["seatMap"]["POIs"] if x["title"]==seatinfo["seat_number"]]
                if len(seat) == 0:
                    res["status"] = False
                    res["message"] = "座位不存在"
                    return res
                else:
                    data = {}
                    data["beginTime"] = str(dt.datetime.strptime(seatinfo["begin_time"], "%Y-%m-%d %H:%M:%S").timestamp())
                    data["duration"] = str(seatinfo["duration"])
                    data["seats[0]"] = seat[0]["id"]
                    data["seatBookers[0]"] = self.user_info["id"]
                    seatinfo["data"] = data
                    status_dict = {
                        "0":"空座位",
                        "1":"已被选",
                        "3":"被ban"
                    }
                    seatinfo["status"] = "未被ban" if str(seat[0]["state"]) != "3" else "被ban"
                    self.seat_list.append(seatinfo)
                    res["status"] = True
                    res["message"] = "成功"
                    return res

    def update_config(self):
        """
        更新配置文件
        """
        self.config["user_info"] = self.user_info
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
    
    def run(self):
        res = {"status": None, "message": None}
        interval = self.settings["interval"]
        max_try_times = self.settings["max_try_times"]
        for _ in range(max_try_times):
            for seat in self.seat_list:
                data = seat["data"]
                url = self.urls["book_seat"]
                response = self.session.post(url, data=data).json()
                if response["CODE"] == "ok":
                    res["status"] = True
                    res["message"] = "预约成功"
                    res["seat_info"] = seat
                    return res
                sleep(interval)
        res["status"] = False
        return res
            
    
