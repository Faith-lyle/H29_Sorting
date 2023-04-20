#!/usr/bin/python3
# -*- encoding: utf-8 -*-
"""
@Name: H29_Sorting>>main.py
@Auth: long.hou
@Email: long.hou2@luxshare-ict.com
@Date: 2023/4/18-13:57
@IDE: PyCharm 
"""
import json
import os
import sys
import time
import uuid
from Tool import serialPort
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import Qt
from GUI.mainPanel import MainPanel
from Tool.logger import logger, ConsolePanelHandler, set_file_log_path
from Tool.runThread import RunThread

# 电脑MAC地址


mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
mac = ":".join([mac[e:e + 2] for e in range(0, 11, 2)]).upper()


def read_json():
    if not os.path.exists('./Config/config.json'):
        exit()
    with open('./Config/config.json', 'r') as f:
        data = json.load(f)
    data['MesConfig']['mac_address'] = mac
    return data


def sava_json(data):
    with open('./Config/config.json', 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def main_close_signal_slot(panel_data):
    config['panel'] = panel_data
    sava_json(config)
    term.close_port()
    run_thread.quit()


is_test = False
wait_time = 0


def main_timer_timeout_slot():
    global is_test, wait_time
    if term.port.is_open and not is_test:
        r = term.send_and_read_no_log('ft module clr\n', 0.2)
        r += term.send_and_read_no_log('a\n', 0.2)
        logger.info("Check connect:{}".format(r))
        main.lineEdit.setText("")
        main.label_6.setText("")
        main.label_5.setText("")
        main.label_4.setText("")
        # main.lineEdit.setStyleSheet('')
        if r:
            if wait_time == 0:
                is_test = True
                main.label_6.setText("TESTING")
                main.label_6.setStyleSheet('background-color:yellow')
                main.textEdit.clear()
                user_path = f"{os.path.expanduser('~')}/logs"  # 获取用户路径
                if not os.path.exists(user_path):
                    os.mkdir(user_path)
                dir_path = os.path.join(user_path, time.strftime("%Y-%m-%d"))
                if not os.path.exists(dir_path):
                    os.mkdir(dir_path)
                set_file_log_path('{}/{}.log'.format(dir_path, time.strftime("%H-%M-%S")))
                run_thread.set_args(config, logger, term, '{}/{}.log'.format(dir_path, time.strftime("%H-%M-%S")))
                # time.sleep(0.5)
                run_thread.start()
            else:
                wait_time -= 1

        else:
            main.label_6.setText("Unconnected Product".upper())
            main.label_6.setStyleSheet('background-color: rgb(106, 255, 253);color:yellow')
            logger.info("Not read production")


def main_signal_connect():
    main.close_signal.connect(main_close_signal_slot)
    main.timer.timeout.connect(main_timer_timeout_slot)


def thread_signal_connect():
    run_thread.content_signal.connect(main.write)
    run_thread.retest_signal.connect(response_run_thread_retest_signal)
    run_thread.test_result_signal.connect(response_run_thread_result_signal)


def response_run_thread_retest_signal():
    global is_test, wait_time
    is_test = False
    wait_time = config['panel']['waitTime']


def response_run_thread_result_signal(data):
    main.update_SerialNumber_Result(data)


def open_serial():
    try:
        serial_p = serialPort.SerialPort(config['panel']['serial_port'], logger)
        return serial_p
    except Exception as e:
        QMessageBox.critical(None, "Erroe", "Open Serial Port Failed, Error Message:{}".format(e))
        exit(0)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    config = read_json()
    main = MainPanel(config['panel'])
    # 设置窗体置顶
    main.setWindowFlag(Qt.WindowStaysOnTopHint)
    term = open_serial()
    run_thread = RunThread(parent=main)
    handler = ConsolePanelHandler(run_thread)
    logger.addHandler(handler)
    main_signal_connect()
    thread_signal_connect()
    main.show()
    sys.exit(app.exec())
