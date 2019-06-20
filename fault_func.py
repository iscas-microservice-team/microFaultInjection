#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import time
import sys
import logging


# 按照不同模式增长,1线性，2指数
def cal(num, dif, mode):
    num = int(num)
    if int(mode) == 1:
        num = num + dif
    elif int(mode) == 2:
        num = num * 2
    return str(num)


def fault_injection():
    print("fault_injection func")
    env_dict = os.environ
    # fault_list = {'cpu' : 1, 'mem' : 2, 'disk' : 3, 'net' : 4}
    fault_type = env_dict.get('FAULT_TYPE') or 'cpu'
    # cpu : FAULT_TYPE、THREAD_NUM、MODE
    # mem : FAULT_TYPE、THREAD_NUM、MEM_SIZE、MODE
    # disk : FAULT_TYPE、THREAD_NUM、MODE
    # net : FAULT_TYPE、NET_PORT、MODE
    if fault_type == 'cpu':
        print("cpu error injection")
        logging.info(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        logging.info("cpu error injection success!")
        thread_num = env_dict.get('THREAD_NUM') or '4'
        duration = env_dict.get('DURATION') or '100'
        # mode = env_dict.get('MODE') or '1'
        print("stress -c %s -t %s" %(thread_num, duration))
        os.system("stress -c %s -t %s" %(thread_num, duration))
    elif fault_type == 'mem':
        logging.info(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        logging.info("mem error injection success!")
        thread_num = env_dict.get('THREAD_NUM') or '4'
        mem_size = env_dict.get('MEM_SIZE') or '5M'
        duration = env_dict.get('DURATION') or '100'
        # mode = env_dict('MODE') or '1'
        os.system("stress --vm %s --vm-bytes %s --vm-keep -t %s" %(thread_num, mem_size, duration))
    # iostat -x -k -d 1
    elif fault_type == 'disk':
        logging.info(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        logging.info("disk error injection success!")
        io_times = env_dict.get("IO_TIMES") or '4'
        duration = env_dict.get('DURATION') or '100'
        # mode = env_dict('MODE') or '1'
        os.system("stress -i %s -t %s" % (io_times, duration))
    elif fault_type == 'net':
        logging.info(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        logging.info("net error injection success!")
        net_port = env_dict.get('NET_PORT')
        if not env_dict.get('NET_FLAG'):
            os.system("iperf3 -s -p %s" % (net_port))
        os.system("export NET_FLAG=1")


if __name__ == '__main__':
    while True:
        print("main func")
        env_dict = os.environ
        # kill为true，则停止循环
        kill = env_dict.get('KILL') or 'false'
        if kill == 'true':
            break
        # flag标记是否需要注入故障
        flag = env_dict.get('FLAG') or 'false'
        logging.info(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        logging.info("excute main()!")
        if flag == 'true':
            time.sleep(2)
            os.environ['FLAG'] = 'false'
            fault_injection()
        time.sleep(5)

