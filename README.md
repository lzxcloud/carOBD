## 该成程序用于读取车内信息，可配合手机app实现相关功能
由python-obd 开发而来

### 使用方法
安装memcache
守护进程supervisord配置如下

```
[program:carinfo]
directory = /home/pi/carOBDPI
command =python3 carinfo.py
autostart = true
startsecs = 5
autorestart = true
startretries = 3     ; 启动失败自动重试次数，默认是 3
user = pi
redirect_stderr = true  ; 把 stderr 重定向到 stdout，默认 false
stdout_logfile_maxbytes = 20MB  ; stdout 日志文件大小，默认 50MB
stdout_logfile_backups = 20     ; stdout 日志文件备份数
; stdout 日志文件，需要注意当指定目录不存在时无法正常启动，所以需要手动创建目录（supervisord 会自动创建日志文件）
stdout_logfile = /var/log/carinfo2_stdout.log

[program:api]
directory = /home/pi/carOBDPI
command =python3 app.py
autostart = true
startsecs = 5
autorestart = true
startretries = 3     ; 启动失败自动重试次数，默认是 3
user = pi
redirect_stderr = true  ; 把 stderr 重定向到 stdout，默认 false
stdout_logfile_maxbytes = 20MB  ; stdout 日志文件大小，默认 50MB
stdout_logfile_backups = 20     ; stdout 日志文件备份数
; stdout 日志文件，需要注意当指定目录不存在时无法正常启动，所以需要手动创建目录（supervisord 会自动创建日志文件）
stdout_logfile = /var/log/app_stdout.log

[program:sender]
directory = /home/pi/carOBDPI
command =python3 sender.py
autostart = true
startsecs = 5
autorestart = true
startretries = 3     ; 启动失败自动重试次数，默认是 3
user = pi
redirect_stderr = true  ; 把 stderr 重定向到 stdout，默认 false
stdout_logfile_maxbytes = 20MB  ; stdout 日志文件大小，默认 50MB
stdout_logfile_backups = 20     ; stdout 日志文件备份数
; stdout 日志文件，需要注意当指定目录不存在时无法正常启动，所以需要手动创建目录（supervisord 会自动创建日志文件）
stdout_logfile = /var/log/sender_stdout.log
```
- 在app.py 配置 memcache地址 默认本机
- carinfo.py 配置 memcache地址 默认本机
- 在sender.py 中修改接收数据的服务器的地址


### 运作方式
各个文件独立运行互不影响因此需要第三方软件交互通信这里使用memcache


### 文件介绍
#### app.py
对外提供web查询的接口 
#### carinfo.py
获取obd信息保存到缓存中
#### sender.py
发送信息到服务器