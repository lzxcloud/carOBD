## 该成程序用于读取车内信息，可配合手机app实现相关功能
由python-obd 开发而来

### 使用方法
####配置蓝牙连接 将蓝牙obd连接到串口上

sudo rfcomm bind 0 DC:0D:30:47:76:43 1 

#### 安装memcache

#### 守护进程supervisord 或者在rc.local 配置自启动
python3 你的路径 + /carOBD/backend/carinfo.py

在setting中配置想要查询的命令 命令表见python-obd

- 在backend/carinfo.py 配置 memcache地址 默认本机
- 在sender.py 中修改接收数据的服务器的地址


### 运作方式
各个文件独立运行互不影响因此需要第三方软件交互通信这里使用memcache

### 文件介绍

#### dashboard 
django编写的网页控制台
#### carinfo.py
获取obd信息保存到缓存中
#### sender.py
发送信息到服务器