# ! /usr/bin/python
# -*- coding:utf-8 -*-
# Filename: csv_exporter.py
# Author: jack
# E-mail: jack_chen@subin.cn
# Date: 2016-06-22
# Description: 定时导出csv任务

import time
from apscheduler.scheduler import Scheduler
from ftp_helper import FTPSync
from csv_builder import build_csv
from config import *
from logger import *


scheduler = Scheduler(daemonic=False)


# @scheduler.cron_schedule(second='*', day_of_week='0-6', hour='8-12,13-24')
# def _quote_send_sh_job():
#     print('a simple cron job start at', datetime.datetime.now())


@scheduler.interval_schedule(hours=export_csv_interval,
                             start_date=time.strftime('%Y-%m-%d', time.localtime(time.time())) + ' ' + export_csv_time)
def _timer_export():
    _export(1)


def auto_export_csv():
    # 启动服务导出前某天报表
    for beforeday in export_before_days:
        _export(beforeday)
    scheduler.start()

def _export(before_day):
    try:
        csv_file = build_csv(before_day)
        ftp = FTPSync(ftp_ip)
        ftp.login(ftp_name, ftp_psw)
        #ftp.list_file(ftp_path) # 查看当前FTP路径下文件
        #ftp.delete_file(ftp_path) # 删除5天前数据
        for csv in csv_file:            # 两个csv文件
            ftp.put_file('file/' + csv, ftp_path) #
    except Exception as e:
        print(e)
        logging.exception(e)
