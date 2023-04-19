#!/usr/bin/python3
# -*- encoding: utf-8 -*-
"""
@Name: H29_Sorting>>mainPanel.py
@Auth: long.hou
@Email: long.hou2@luxshare-ict.com
@Date: 2023/4/18-13:58
@IDE: PyCharm 
"""

import sys
import os
from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal
from PyQt5.QtGui import QColor

from GUI.UI.mainPanel_ui import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QPushButton, QFormLayout, QDesktopWidget
from PyQt5.QtWidgets import QWidget, QMainWindow
from PyQt5.QtCore import QTimer


class MainPanel(Ui_MainWindow, QMainWindow):
    close_signal = pyqtSignal(dict)

    def __init__(self, config_dict):
        super(MainPanel, self).__init__()
        self.setupUi(self)
        self.reset_btn = QPushButton("Reset")
        self.timer = QTimer(self)
        self.config_dict = config_dict
        self.ui_init()
        self.center()
        self.timer.start(config_dict['updateTime']*1000)

    def center(self):
        # 获取屏幕坐标系
        screen = QDesktopWidget().screenGeometry()
        # 获取窗口坐标系
        size = self.geometry()
        newLeft = screen.width() - size.width()
        newTop = screen.height() - size.height()
        self.move(newLeft/2, newTop/2)

    def ui_init(self):
        self.label.setText(self.config_dict['Title'])
        self.setWindowTitle(self.config_dict["Title"])
        self.formLayout.setWidget(4, QFormLayout.SpanningRole, self.reset_btn)
        try:
            self.add_fail_qty(0)
            self.add_pass_qty(0)
        except ZeroDivisionError:
            self.lb_yield.setText("100%")
        self.reset_btn.clicked.connect(self.clear_count_qty)

    def add_pass_qty(self, qty):
        self.config_dict['PASSQty'] += qty
        self.lb_pass.setText(str(self.config_dict['PASSQty']))
        total = self.config_dict['PASSQty'] + self.config_dict['FAILQty']
        self.lb_yield.setText("{:.2f}%".format(self.config_dict['PASSQty'] / total * 100))

    def add_fail_qty(self, qty):
        self.config_dict['FAILQty'] += qty
        self.lb_fail.setText(str(self.config_dict['FAILQty']))
        total = self.config_dict['PASSQty'] + self.config_dict['FAILQty']
        self.lb_yield.setText("{:.2f}%".format(self.config_dict['PASSQty'] / total * 100))
        # print(self.config_dict['PASSQty'] / total * 100)

    def clear_count_qty(self):
        self.config_dict['FAILQty'] = 0
        self.config_dict['PASSQty'] = 0
        self.lb_pass.setText("0")
        self.lb_fail.setText("0")
        self.lb_yield.setText("100%")

    def update_SerialNumber_Result(self,data):
        print(data)
        self.lineEdit.setText(data['read_product_mlb'])
        self.label_5.setText(data['acccel_test'])
        self.label_4.setText(data['SystemClock_Info_SysClk_80Mhz'])
        self.label_6.setText(data['Test Pass/Fail Status'])
        if data['Test Pass/Fail Status'] == "PASS":
            self.label_6.setStyleSheet('background-color: lime;')
            self.add_pass_qty(1)
        else:
            self.label_6.setStyleSheet('background-color: rgb(255, 8, 9);')
            self.add_fail_qty(1)

    def write(self, msg):
        self.textEdit.append(msg)

    def closeEvent(self, a0):
        self.close_signal.emit(self.config_dict)
        # print(self.config_dict)
        super(MainPanel, self).closeEvent(a0)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainPanel()
    main.show()
    sys.exit(app.exec_())
