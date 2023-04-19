#!/usr/bin/python3
# -*- encoding: utf-8 -*-
"""
@Name: H29_Sorting>>mes.py
@Auth: long.hou
@Email: long.hou2@luxshare-ict.com
@Date: 2023/4/18-14:11
@IDE: PyCharm 
"""
import json
import os
import time

import requests


def read_station_json():
    config = {}
    if os.path.exists('/vault/data_collection/test_station_config/gh_station_info.json'):
        with open('/vault/data_collection/test_station_config/gh_station_info.json', 'r') as f:
            config = json.load(f)['ghinfo']
    return config


class Mes:
    def __init__(self, log):
        self.log = log
        self.config = read_station_json()
        self.url = self.config['SFC_URL']

    def get_SIP_X_num(self, sn):
        result = False, None
        try:
            data = {'p': "SIP_X_NUM", "c": "QUERY_RECORD", "sn": sn}
            response = requests.post(url=self.url, data=data, timeout=3)
            self.log.mes_log(func_name='get_SIP_X_num', url=self.url, data=data, response=response)
            if response.status_code == 200:
                if "SFC_OK" in response.text:
                    l1 = response.text.split("SFC_OK")[1]
                    if 'NO X BOAR' in l1:
                        result = True, []
                    else:
                        result = True, map(int, l1.split(',')[1:])
        except Exception as e:
            result = False, "Run Error\n{}".format(e)
        return result

    def check_process(self, sn):
        result = False, "Process Error\n unit_process_check=UNIT OUT OF PROCESS TERMINAL_NAME ERROR!"
        try:
            data = {'p': "unit_process_check", "c": "QUERY_RECORD", 'sw_version': '1.0.0.1',
                    'tsid': self.config['STATION_ID'], "sn": sn, 'fixture_id': None}
            response = requests.post(url=self.url, data=data, timeout=3)
            self.log.mes_log(func_name="check_process", url=self.url, data=data, response=response)
            if response.status_code == 200:
                if "SFC_OK" in response.text:
                    if response.text.endswith("unit_process_check=OK"):
                        result = True, 'unit_process_check=OK'
                    else:
                        result = False, 'Process Error\n' + response.text.split('::')[-1]
        except Exception as e:
            result = False, "Run Error\n{}".format(e)
        return result

    def update_test_value_to_mes(self, data):
        '''
        :param data: data 为字典，其中要有result<str>，audio_mode<int>,start_time<str>,stop_time<str>,sn<str>,
        fixture_id<int>,test_head_id<int>,list_of_failing_tests<str>,failure_message<str>
        :return:
        '''
        result = False
        send_data = {
            'c':'ADD_RECORD',
            'sw_version':'1.0.0.1',
            'product':self.config['PRODUCT'],
            'station_id':self.config['STATION_ID'],
            'test_station_name':self.config['GH_STATION_NAME'],
            'mac_address':self.config['MAC'],
            'result':data['Test Pass/Fail Status'],
            'audio_mode':0,
            'start_time':data['StartTime'],
            'stop_time':time.strftime("%Y-%m-%d %H:%M:%S"),
            'sn':data['SerialNumber'],
            'fixture_id':data['WorkStationNumber'],
            'test_head_id':data['SlotNumber'],
            'list_of_failing_tests':data['List of Failing Tests'],
            'failure_message':data['List of Failing Tests'].split(';\n')[0]
        }
        try:
            response = requests.post(url=self.url, data=send_data, timeout=3)
            self.log.mes_log(func_name='update_test_value_to_mes', url=self.url, data=send_data, response=response)
            if response.status_code == 200:
                if "SFC_OK" in response.text:
                    result = True
        except Exception as e:
            self.log.mes_error_log(func_name='update_test_value_to_mes', url=self.url, data=send_data, error=e)
            result = False
        return result


if __name__ == '__main__':
    print(read_station_json().keys())
