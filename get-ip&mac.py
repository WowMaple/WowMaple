
import os
import re
import time

file_dir = os.getcwd() + '\\check'        # 待查找文件的目录

get_time = time.strftime("%Y-%m-%d %H_%M_%S", time.localtime())     # 获取当前时间
os.makedirs(os.getcwd() + '\\logs\\' + get_time)                    # 创建本次日志目录

for root, dirs, files in os.walk(file_dir):
    for file_name in files:
        with open(file_dir + '\\' + file_name, 'r', encoding='utf-8') as f:
            content = f.read()
        mac_address = re.findall(r'\w{4}\.\w{4}\.\w{4}', content)                 # 获取所有MAC地址
        mac_address1 = re.findall(r'\w{4}\-\w{4}\-\w{4}', content)                 # 获取所有MAC地址
        mac_address2 = re.findall(r'\w{2}:\w{2}:\w{2}:\w{2}:\w{2}:\w{2}', content)  # 获取所有MAC地址
        with open(os.getcwd() + '\\logs\\' + get_time + '\\[' + file_name + ']---文件中的IP地址与MAC地址.txt', 'a',
                  encoding='utf-8') as f:
            print(file_name + '---此文件中的MAC地址有：')
            f.write('MAC地址：\n')
            for i in mac_address:
                print(i)
                f.write(i + '\n')
            for i in mac_address1:
                print(i)
                f.write(i + '\n')
