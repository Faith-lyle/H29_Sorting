#!/usr/bin/python3
# -- coding: utf-8 --
# @Author : Long.Hou
# @Email : Long2.Hou@luxshare-ict.com
# @File : demo.py
# @Project : H29_Sorting
# @Time : 2023/4/18 16:07
# -------------------------------
import re
text ='''
00007968 [ pmu] ERR !volt1 fail:0xff
00007971 [ pmu] Volt OOB:-7mV
00007971 [ pmu] Init Algos Failed
> accel:ok +X:00003457,+Y:00005310,+Z:00001212,-X:-0003975,-Y:-0002686,-Z:-0004099
]
] '''

pattern = re.compile(r'X:(\-|\+)?\d*')

print(pattern.search(text))
a = re.findall(r'X:(\-|\+)?(\d*)',text)
b = ('/Users/luxshare-ict/logs/2023-04-19.log'.split('/'))
c = '/'.join(b[:-1])
print(c)
# print(next(a).group())


# text = text.replace('\n','')
# text = text.replace('+X','')
# text = text.replace('-X','')
# print(text.split(','))
# a = float("00003457")
# b = float('-0003975')
# xValue = a-b
# v = xValue*0.488/1000
# print(v)
if __name__ == '__main__':
    ...
