# 微服务"错误注入Sidecar"使用说明文档
> 作者: 中科院软件所微服务研究项目小组

> 该项目作者: github.com/XinyaoTian || leontian1024@gmail.com

## 项目概述

本项目意在构建一个专注于对微服务最小单元进行错误注入的独立服务。

将本项目的代码以容器的形式与实际微服务应用部署在同一个微服务单元中，
通过该模块所提供的 REST API 向其中注入包括"cpu、内存、磁盘和网络"等多种错误，
对微服务最小单元的资源利用情况进行实验和观测。

## 运行条件

本项目基于 Linux Distribution 操作系统的多种命令进行错误注入，
若想在本地直接运行本项目，请确保满足以下条件:

1. 操作系统必须为 Linux Distribution (本项目在 Ubuntu 16.04 系统上通过测试)
2. 具有 python3.7 运行环境以及相应的 Flask, Flask-wtf,flask-bootstrap 工具库 
3. 安装了 stress 命令工具
4. 安装了 iperf3 命令工具
5. 确保设备的 5000 端口未被占用

或使用 dockerhub 获取我们封装好的镜像，并在容器内部映射 5000 端口至外部

```bash
# 使用 docker 简单测试该应用( docker 版本需高于 18.03-ce )
docker run --rm -it -d --name fault-injection-server -p 5000:5000  xinyaotian/micro-fault-injection:1.0.0
```

同样，你也可以利用本项目根目录下的 Dockerfile 自行进行封装

封装命令如下:
```bash
# 首先需进入该项目的目录 microFaultInjection/ 中, 再运行下面的命令
docker build -t your-docker-name/project-name:1.0 .
```

## 使用方法
>备注: 本"使用方法"亦可在启动服务后，通过服务的 / 或 /usage 这两种 url 进行查看

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
> 项目根目录下的 single_fault_injection.yaml 可以直接将本应用
> 以 Deployment 的形式部署在 K8s 或 Istio 上;
> 并对外暴露 30050 端口

```bash
# 直接通过 yaml 部署于 K8s 或 Istio (K8s 版本 1.13.1 / Istio 1.0.6 通过测试)
kubectl apply -f ./fault-server.yaml
```

本项目的镜像将作为原本微服务应用的 Sidecar 独立部署运行，
因此在 K8s 环境中其应该与业务应用部署于同一个 Pod 之中。

在 K8s 环境下部署和启动的 yaml 如下所示意( Istio 同样可以这样写 ):

```yaml

---
# 为 fault injection 创建 service 分配端口 #
---
apiVersion: v1
kind: Service
metadata:
  name: your-microapp-with-faultinjection
  namespace: default
spec:
  selector:
    # deployment identifier
    # 这个标签要与 deployment 中相对应
    app: sidecar-fault-injection
  ports:
    - protocol: TCP
      port: 5000
      nodePort: 30050
  type: NodePort
---
# 相应的 deployment 配置( 与原应用配置在一起 )
---
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: your-microapp-with-faultinjection
  namespace: default
spec:
  replicas: 1
  template:
    metadata:
      labels:
        # svc identifier
        # 这个标签要与 service 中相对应
        app: sidecar-fault-injection
    spec:
      containers:
      # 你原来应用的 container 信息
      - name: your-micro-app
        image: your-docker-name/project:1.0
        imagePullPolicy: IfNotPresent
        env:
        - name: PATH_VALUE
          value: "example"
        ports:
        - containerPort: 80
      # ------------------- #
      # Sidecar 错误注入模块的 container
      - name: fault-injection-sidecar
        image: xinyaotian/micro-fault-injection:1.0.0
        imagePullPolicy: IfNotPresent
        ports:
        - containerPort: 5000
      # ------------------- #
---

```

