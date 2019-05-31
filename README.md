## Flask部署
### 1. 环境
* OS：CentOS7 x86_64
* Python: 3.6
* Flask: 1.0
* uwsgi: 2.0
* Nginx或Openresty
* MySQL: 5.7.26
### 2. 安装Python36
```bash
yum install python36-devel
```
### 3. 创建并激活虚拟环境
```bash
python3 -m venv venv
. venv/bin/activate
```
### 4. 安装依赖
```bash
yum install gcc
```
### 5. 安装uwsgi
```bash
pip install uwsgi
```
### 6. 安装nginx或openresty
```bash
yum install nginx
yum install openresty
```
### 7. 项目依赖安装
```bash
pip install -r requirements.txt
```
### 8. 在项目目录下添加uwsgi.ini配置
```ini
[uwsgi]
# 套接字通讯端口，相当于为外界留出一个uWSGI服务器的接口，负责与Nginx通信，但注意socket是无法直接通过http请求成功访问
# 服务器端口
socket = 127.0.0.1:5000
#socket = :5000
# 浏览器中http访问
#http = :5000
# 项目目录
pythonpath = /mnt/data/personal/gcs-flask
# 指定项目启动脚本名字
module = start
# 程序内启用的application变量名，一般为app
callable = app
# 处理器个数
processes = 4
# 线程数
threads = 2
# processes和threads指出了启动uwsgi服务器之后，服务器会打开几个并行的进程，每个进程会开几条线程来等待处理请求，显然这个数字应该合理，太小会使得处理性能不好而太大则会给服务器本身带来太大负担。
# 获取uwsgi统计信息的服务地址
#stats = 127.0.0.1:9191
stats = :9191
# 使uWSGI进程在后台运行，并将日志打到指定的日志文件或者udp服务器
daemonize = ./uwsgi.log
pidfile = ./uwsgi.pid
```
### 9. uwsgi启动、停止、重启
```bash
uwsgi --ini uwsgi.ini
uwsgi --stop uwsgi.pid
uwsgi --reload uwsgi.pid
```

### 10. nginx配置
* 创建conf.d文件夹，新建seal.conf文件
* 在nginx.conf配置添加
include /usr/local/openresty/nginx/conf/conf.d/*.conf;
```nginx
upstream flask {
        server 127.0.0.1:5000;
}
server {
        listen 9091;
        charset utf-8;
        location / {
            include /usr/local/openresty/nginx/conf/uwsgi_params;
            uwsgi_pass flask;
            uwsgi_param UWSGI_PYHOME /mnt/data/personal/gcs-flask/venv;
            uwsgi_param UWSGI_CHDIR /mnt/data/personal/gcs-flask;
            uwsgi_param UWSGI_SCRIPT run:start;
        }
```