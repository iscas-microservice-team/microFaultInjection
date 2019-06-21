# 微服务"错误注入Sidecar"使用说明文档
作者: 中科院软件所微服务研究项目小组

## 项目概述

本项目意在构建一个专注于对微服务最小单元进行错误注入的独立服务。

将本项目的代码以容器的形式与实际微服务应用部署在同一个微服务单元中，
通过该模块所提供的 REST API 向其中注入包括"cpu、内存、磁盘和网络"等多种错误，
对微服务最小单元的资源利用情况进行实验和观测。

## 运行条件

本项目基于 Linux Distribution 操作系统的多种命令进行错误注入，
若想在本地直接运行本项目，请确保满足以下条件:

1. 操作系统必须为 Linux Distribution (本项目在 Ubuntu 16.04 系统上通过测试)
2. 具有 python3.7 运行环境以及相应的 flask, python-dotenv 工具库 
3. 安装了 stress 命令工具
4. 安装了 iperf3 命令工具
5. 确保设备的 5000 端口未被占用

或使用 dockerhub 获取我们封装好的镜像，并在容器内部映射 5000 端口至外部

该项目镜像的 DockerHub 地址:


## 使用方法

本项目基于 REST API 理念进行设计，故进行错误注入时需使用 POST 方式，
向指定 url 发送注入信息。

错误注入的 POST 请求发送示例如下( 注意改变 IP 与端口号 ):

1. 注入 CPU 故障

```bash
# fault_type=cpu 指定错误故障类型(此处为 cpu 类型)
# thread_num=4 触发该错误的线程数(此处为 4 个线程)
# duration=15 故障持续时间,单位为秒(此处为 15 秒)
curl -X POST -d 'fault_type=cpu&thread_num=4&duration=15' http://localhost:5000/fault-inject
```

2. 注入内存故障

```bash
# fault_type=mem 指定错误故障类型(此处为 mem 类型)
# mem_size=120M 指定内存泄露的数值(此处为 120M ,注意 M 不能省略)
# thread_num=4 触发该错误的线程数(此处为 4 个线程)
# duration=15 故障持续时间,单位为秒(此处为 15 秒)
curl -X POST -d 'fault_type=mem&mem_size=120M&thread_num=4&duration=15' http://localhost:5000/fault-inject
```

3. 注入磁盘故障

```bash
# fault_type=disk 指定错误故障类型(此处为 disk 类型)
# io_times=4 
# duration=15 故障持续时间,单位为秒(此处为 15 秒)
curl -X POST -d 'fault_type=disk&io_times=4&duration=15' http://localhost:5000/fault-inject
```

4. 注入网络故障

```bash
# fault_type=net 指定错误故障类型(此处为 net 类型)
# net_port=100
curl -X POST -d 'fault_type=net&net_port=100' http://localhost:5000/fault-inject
```

## Yaml编写示例( 以 Sidecar 形式将本项目部署于微服务中 )

