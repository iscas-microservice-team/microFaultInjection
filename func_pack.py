# -*- coding: UTF-8 -*-
import os
import time
import logging


# 将薛师兄代码里的数字转变为更加易懂的参数输入
def fault_injection(fault_type, **kwargs):
    logging.info("Ready to inject fault.")
    # fault_type have 4 types: 'cpu', 'mem', 'disk', 'net'
    if fault_type == 'cpu':
        print("cpu error injection")
        logging.info(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        # CPU Fault has 2 args: thread_num, duration
        if 'thread_num' not in kwargs or kwargs['thread_num'] is None:
            thread_num = '4'
        else:
            thread_num = kwargs['thread_num']
        if 'duration' not in kwargs or kwargs['duration'] is None:
            duration = '100'
        else:
            duration = kwargs['duration']
        # 切分为多进程
        pid = os.fork()
        # 子进程负责错误注入
        if pid == 0:
            # using linux command to inject faults.
            os.system("stress -c %s -t %s" % (thread_num, duration))
        # 父进程负责返回注入结果并继续监听 Server 端口
        else:
            logging.info("stress -c %s -t %s" % (thread_num, duration))
            info = [
                {'status': 'success'},
                {'description': 'Your arguments of injection are thread_num=%s, duration=%s.' % (thread_num, duration)}
            ]
            return info

    elif fault_type == 'mem':
        logging.info(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        # Memory Fault has 3 args: thread_num, mem_size, duration
        if 'thread_num' not in kwargs or kwargs['thread_num'] is None:
            thread_num = '4'
        else:
            thread_num = kwargs['thread_num']
        if 'mem_size' not in kwargs or kwargs['mem_size'] is None:
            mem_size = '128M'
        else:
            mem_size = kwargs['mem_size']
        if 'duration' not in kwargs or kwargs['duration'] is None:
            duration = '100'
        else:
            duration = kwargs['duration']

        os.system("stress --vm %s --vm-bytes %s --vm-keep -t %s" % (thread_num, mem_size, duration))
        return None

    # iostat -x -k -d 1
    elif fault_type == 'disk':
        logging.info(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        # args
        if 'io_times' not in kwargs or kwargs['io_times'] is None:
            io_times = '4'
        else:
            io_times = kwargs['io_times']
        if 'duration' not in kwargs or kwargs['duration'] is None:
            duration = '100'
        else:
            duration = kwargs['duration']

        os.system("stress -i %s -t %s" % (io_times, duration))
        return None

    elif fault_type == 'net':
        logging.info(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        if 'net_port' not in kwargs or kwargs['net_port'] is None:
            net_port = '100'
        else:
            net_port = kwargs['net_port']

        os.system("iperf3 -s -p %s" % net_port)
        return None

    # 若错误类型不在这4种之内，则返回 None
    else:
        error = [
            {'status': 'error'},
            {'description': 'fault_type must in the range of cpu, mem, dish and net. Your fault_type is %s.' % fault_type}
        ]
        return error

    pass


if __name__ == '__main__':
    fault_injection('cpu')

