# -*- coding: utf-8 -*-

import psutil
import datetime
import time
import os

Prefix = '!!status'
WorldPath = './server/world'

def on_info(server ,info):
    content = info.content
    command = content.split(' ')
    if len(command) == 0 or command[0] != Prefix:
        return
    del command[0]
    
    if not info.is_user:
        return
        
    if len(command) == 0:
        print_message(server,info)
    
def on_load(server ,old):
    server.add_help_message('!!status', '获取服务器状态信息')
    
    
def print_message(server,info):    
    server.reply(info ,'获取系统信息中，请稍后...', encoding=None)
    server.reply(info ,'---------常规信息---------', encoding=None)
    # 当前时间
    now_time = time.strftime('系统时间:§e%Y-%m-%d-%H:%M:%S', time.localtime(time.time()))
    server.reply(info, now_time, encoding=None)

    # 查看cpu物理个数的信息
    server.reply(info ,u"物理CPU个数: §e%s §r逻辑CPU个数: §e%s " % (psutil.cpu_count(logical=False) ,psutil.cpu_count()), encoding=None)

    #CPU的使用率
    cpu = (str(psutil.cpu_percent(1))) + '%'
    server.reply(info ,u"CPU使用率:§e %s" % cpu, encoding=None)

    #查看内存信息,剩余内存.free  总共.total
     
    free = str(round(psutil.virtual_memory().free / (1024.0 * 1024.0 * 1024.0), 2))
    total = str(round(psutil.virtual_memory().total / (1024.0 * 1024.0 * 1024.0), 2))
    memory = int(psutil.virtual_memory().total - psutil.virtual_memory().free) / float(psutil.virtual_memory().total)
    server.reply(info ,u"物理内存：§e %s G" % total, encoding=None)
    server.reply(info ,u"剩余物理内存：§e %s G" % free, encoding=None)
    server.reply(info ,u"物理内存使用率：§e %s %%" % int(memory * 100), encoding=None)
    # 系统启动时间
    server.reply(info ,u"系统启动时间:§e %s" % datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S"), encoding=None)

    #网卡，可以得到网卡属性，连接数，当前流量等信息
    net = psutil.net_io_counters()
    bytes_sent = '{0:.2f} Mb'.format(net.bytes_recv / 1024 / 1024)
    bytes_rcvd = '{0:.2f} Mb'.format(net.bytes_sent / 1024 / 1024)
    server.reply(info ,u"网卡接收流量§e %s §r网卡发送流量§e %s" % (bytes_rcvd, bytes_sent), encoding=None)

    server.reply(info ,'---------存档信息---------', encoding=None)
    WorldSize = getFileSize(WorldPath)
    server.reply(info ,'存档大小§e {0:.2f} §rMB'.format(WorldSize / 1024 / 1024), encoding=None)
    
    

def getFileSize(filePath, size=0):
    for root, dirs, files in os.walk(filePath):
        for f in files:
            size += os.path.getsize(os.path.join(root, f))
    return size