#!/usr/bin/python3
# -*- encoding: utf-8 -*-
"""
@Name: H29_Sorting>>runThread.py
@Auth: long.hou
@Email: long.hou2@luxshare-ict.com
@Date: 2023/4/18-14:10
@IDE: PyCharm 
"""
import os
import time, json
from PyQt5.QtCore import QThread, pyqtSignal
from Tool.functions import TestFunctions, write_csv
from Tool.logHelper import LogHelper
from Tool.mes import Mes


def read_station_json():
    config = {}
    if os.path.exists('/vault/data_collection/test_station_config/gh_station_info.json'):
        with open('/vault/data_collection/test_station_config/gh_station_info.json', 'r') as f:
            config = json.load(f)['ghinfo']
    return config


class RunThread(QThread):
    test_result_signal = pyqtSignal(dict)
    content_signal = pyqtSignal(str)

    def __init__(self, parent):
        super().__init__(parent)
        self.func = None
        self.log = None
        self.config_json = None

    def set_args(self, config=None, log=None, term=None):
        self.log = LogHelper(log)
        self.config_json = config
        self.func = TestFunctions(self.log, term=term)
        # print(self.log)

    def write(self, msg):
        self.content_signal.emit(msg)

    def run(self):
        self.log.show_infomation("START TEST, PARSE PARAMETERS SUCCESSFULLY!")
        self.log.show_infomation("Load Test Plan Successfully! Test Plan as below:")
        for item in self.config_json['testPlan']:
            self.log.show_infomation(str(item))
        self.main()

    def main(self):
        result_dict = {'StartTime': time.strftime("%Y-%m-%d %H:%M:%S"),
                       'UnitNumber': 'None',
                       "SerialNumber": "None", 'SlotNumber': 1, 'WorkStationNumber': 1}
        if self.config_json['MesConfig']['GH_info']:
            json_data = read_station_json()
            result_dict['Product'] = json_data['PRODUCT']
            result_dict['Station ID'] = json_data['STATION_ID']
            result_dict['Version'] = '1.0.0.1'
            result_dict['test_station_name'] = json_data['GH_STATION_NAME']
            result_dict['mac_address'] = json_data['MAC']
            result_dict['Site']= json_data["SITE"]
        else:
            result_dict['Product'] = self.config_json["MesConfig"]['product']
            result_dict['Station ID'] = self.config_json["MesConfig"]['station_id']
            result_dict['Version'] = self.config_json["MesConfig"]['sw_version']
            result_dict['test_station_name'] = self.config_json["MesConfig"]['test_station_name']
            result_dict['mac_address'] = self.config_json["MesConfig"]['mac_address']
            result_dict['Site'] = 'ITJX'
        fail_list = {}
        # result_data = {}
        # 测试部分
        for i, item in enumerate(self.config_json['testPlan']):
            try:
                result, value = self.func.choose_function(item['testItem'], *item['Input'])
                self.test_value_signal.emit(i, result, value)
                # result_data[item['testItem']] = value
                if result:
                    if item['testItem'] == 'read_product_mlb':
                        result_dict['SerialNumber'] = value
                    result_dict[item['testItem']] = value
                    result_dict['Test Pass/Fail Status'] = 'PASS'
                else:
                    result_dict['Test Pass/Fail Status'] = 'FAIL'
                    result_dict[item['testItem']] = value
                    fail_list[item['testItem']] = 'Upper:NA,Lower:NA,Value:{}'.format(value)
                time.sleep(0.1)
            except Exception as msg:
                self.log.show_error("Test Item:" + item['testItem'] + "\nError Message:" + str(msg))
                result_dict[item['testItem']] = "FAIL"
                result_dict['Test Pass/Fail Status'] = 'FAIL'
                continue
        # 测试结束，发送退出信号
        for _ in range(3):
            try:
                user_path = f"{os.path.expanduser('~')}/logs"  # 获取用户路径
                if not os.path.exists(user_path):
                    os.mkdir(user_path)
                write_csv('{}/{}.csv'.format(user_path, time.strftime("%Y-%m-%d")),
                          result_dict, self.config_json['testPlan'])
                break
            except Exception as e:
                self.log.show_error("Write CSV Error:" + "\nError Message:{}".format(e))
                time.sleep(0.05)
        self.test_result_signal.emit(result_dict)
        mes = Mes(self.log)
        mes.update_test_value_to_mes(result_dict)
