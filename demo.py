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

text1 = '''
 ft measure sysclk
> ft:ok Sys Clk Freq - Raw:2432, MHz:79.69, Err:-0.38%'''
flag = re.findall(r'MHz:(.*)?, Err:', text1)
print(flag)
if len(flag) == 1:
    if 79.2 < float(flag[0]) < 80.8:
        result = True, flag[0]
pattern = re.compile(r'X:(\-|\+)?\d*')

flag = re.findall(r'(\-|\+)X:(.*)?Y,', text)
print(flag)
if len(flag) == 2:
    v = (float(flag[0][1]) - float(flag[1][1])) * 0.488 / 1000
    if 0.8 < v < 5:
        result = True, v

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
