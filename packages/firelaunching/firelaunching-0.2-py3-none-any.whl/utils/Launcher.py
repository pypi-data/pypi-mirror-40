#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'yuhaiyang'
__mtime__ = '2018-10-08 13:45'
# code is far away from bugs with the god animal protecting
    I love animals. They taste delicious.
              ┏┓      ┏┓
            ┏┛┻━━━┛┻┓
            ┃      ☃      ┃
            ┃  ┳┛  ┗┳  ┃
            ┃      ┻      ┃
            ┗━┓      ┏━┛
                ┃      ┗━━━┓
                ┃  神兽保佑    ┣┓
                ┃　永无BUG！   ┏┛
                ┗┓┓┏━┳┓┏┛
                  ┃┫┫  ┃┫┫
                  ┗┻┛  ┗┻┛
"""
import socket


def udp_socket():
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return udp


def tcp_socket():
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    return tcp


if __name__ == '__main__':
    sk = tcp_socket()
    sk.connect((r"192.168.10.207", 8080))
    data = input('请输入给服务器发送的数据：')
    sk.send(data.encode("utf-8"))
    info = sk.recv(1024)
    print("服务器说：", info.decode("utf-8"))
    sk.close()
