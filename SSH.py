

import paramiko
import time
import socket
import os

with open('Config.txt', 'r', encoding='utf-8') as f:   # 获取配置信息
    config_list = f.readlines()
username = config_list[0].strip()                           # 账号
password = config_list[1].strip()                           # 密码
port = int(config_list[2].strip())                          # 端口号
timeout = int(config_list[3].strip())                       # 登录超时时间
interval = int(config_list[4].strip())                      # 命令执行时间间隔

with open('IPList.txt', 'r', encoding='utf-8') as f:                     # 获取IP列表
    ip_list = f.readlines()

with open('CommandList.txt', 'r', encoding='utf-8') as f:                # 获取执行命令
    cmd_list = f.readlines()

get_time = time.strftime("%Y-%m-%d %H_%M_%S", time.localtime())     # 获取当前时间
os.makedirs(os.getcwd() + '\\logs\\' + get_time)                    # 创建本次日志目录

log_list = []                                    # 定义用于存放日志的列表
login_failed_list = []                           # 定义用于存放登录失败的IP地址的列表
unable_to_connect_list = []                      # 定义用于存放无法连通的IP地址的列表

for line in ip_list:
    try:
        ip = line.strip()
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=ip, port=port, username=username, password=password, timeout=timeout,
                           look_for_keys=False)
        print("已成功登录：", ip + '，开始执行脚本！')
        command = ssh_client.invoke_shell()
        for line1 in cmd_list:
            command.send(line1 + "\n")
            print(line1.strip())
            time.sleep(interval)
            output = command.recv(65535).decode()    # 单次最大接收65535字节（byte），每读取一次都会清空
            log_list.append(output)
        n = 1
        for i in log_list:
            with open(os.getcwd() + '\\logs\\' + get_time + '\\' + str(n) + '.txt', 'a',
                      encoding='utf-8') as f:  # 日志文件
                f.write(i)
            n = n+1
        log_list = []
        ssh_client.close()
    except paramiko.ssh_exception.AuthenticationException:
        print(ip + "，登录失败！")
        login_failed_list.append(ip)
    except socket.error:
        print(ip + "，无法连通！")
        unable_to_connect_list.append(ip)

print('\n【异常情况统计】')
print('登录失败的设备：')

if login_failed_list:
    with open(os.getcwd() + '\\logs\\' + get_time + '\\LoginFailed ' + get_time + '.txt', 'a',
              encoding='utf-8') as f:
        for i in login_failed_list:
            print(i)
            f.write(i + '\n')
else:
    print('无')

print('无法连通的设备：')
if unable_to_connect_list:
    with open(os.getcwd() + '\\logs\\' + get_time + '\\UnableToConnect ' + get_time + '.txt', 'a',
              encoding='utf-8') as f:
        for i in unable_to_connect_list:
            print(i)
            f.write(i + '\n')
else:
    print('无')

print('\n执行完毕，详细操作日志与异常日志，请到logs文件夹中查阅。')
input('\nPress <enter> to exit.')
