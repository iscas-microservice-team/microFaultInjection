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
        thread_num = kwargs['thread_num'] or '4'
        duration = kwargs['duration'] or '100'
        logging.info("stress -c %s -t %s" % (thread_num, duration))
        os.system("stress -c %s -t %s" % (thread_num, duration))

    elif fault_type == 'mem':
        logging.info(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        # Memory Fault has 3 args: thread_num, mem_size, duration
        thread_num = kwargs['thread_num'] or '4'
        mem_size = kwargs['mem_size'] or '5M'
        duration = kwargs['duration'] or '100'
        # mode = env_dict('MODE') or '1'
        os.system("stress --vm %s --vm-bytes %s --vm-keep -t %s" % (thread_num, mem_size, duration))

    # iostat -x -k -d 1
    elif fault_type == 'disk':
        logging.info(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        io_times = kwargs['io_times'] or '4'
        duration = kwargs['duration'] or '100'
        # mode = env_dict('MODE') or '1'
        os.system("stress -i %s -t %s" % (io_times, duration))

    elif fault_type == 'net':
        logging.info(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        net_port = kwargs['NET_PORT']
        # if not env_dict.get('NET_FLAG'):
        if kwargs['net_flag'] is None:
            os.system("iperf3 -s -p %s" % net_port)

    # 若错误类型不在这4种之内，则返回 None
    else:
        return None

    pass


if __name__ == '__main__':
    fault_injection('cpu', thread_num=4, duration=100)

