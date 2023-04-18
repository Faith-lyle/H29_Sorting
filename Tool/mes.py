#!/usr/bin/python3
# -*- encoding: utf-8 -*-
"""
@Name: H29_Sorting>>mes.py
@Auth: long.hou
@Email: long.hou2@luxshare-ict.com
@Date: 2023/4/18-14:11
@IDE: PyCharm 
"""
import requests


def update_test_value_to_mes(data):
    '''
    :param data: data 为字典，其中要有result<str>，audio_mode<int>,start_time<str>,stop_time<str>,sn<str>,
    fixture_id<int>,test_head_id<int>,list_of_failing_tests<str>,failure_message<str>
    :return:
    '''
    result = False
    try:
        for k in self.config.keys():
            data[k] = self.config[k]
        data["c"] = "ADD_RECORD"
        response = requests.post(url=self.url, data=data, timeout=3)
        self.log.mes_log(func_name='update_test_value_to_mes', url=self.url, data=data, response=response)
        if response.status_code == 200:
            if "SFC_OK" in response.text:
                result = True
    except Exception as e:
        self.log.mes_error_log(func_name='update_test_value_to_mes', url=self.url, data=data, error=e)
        result = False
    return result