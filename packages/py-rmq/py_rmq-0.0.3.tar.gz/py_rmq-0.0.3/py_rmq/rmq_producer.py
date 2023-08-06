#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : HaiFeng
# @Email   : 24918700@qq.com
# @Time    : 2019/1/15
# @desc    : desc


import os
import platform
from ctypes import *


class Producer(object):
    '''生产者'''

    def __init__(self, pid: str, access_key: str, secret_key: str):
        '''使用示例 https://gitee.com/haifengat/ali_rmq_api/blob/master/py_rmq/rmq_test.py

        :param pid: producerid PID_xxx
        :param access_key: access key
        :param secret_key: secret key
        '''
        dlldir = os.path.abspath(os.path.dirname(__file__))
        cur_path = os.getcwd()
        os.chdir(dlldir)
        dlldir = os.path.join(dlldir, 'producer.' + ('dll' if 'Windows' in platform.system() else 'so'))
        self.h = CDLL(dlldir)

        self.h.ProducerStart.argtypes = [c_void_p, c_void_p, c_void_p]
        self.h.ProducerStart.restype = c_void_p

        self.h.ProducerShutdown.argtypes = [c_void_p]
        self.h.ProducerShutdown.restype = None

        self.h.ProducerSendMsg.argtypes = [c_void_p, c_void_p, c_void_p, c_void_p, c_void_p, c_int]
        self.h.ProducerSendMsg.restype = c_char_p

        self.producer = self.h.ProducerStart(bytes(pid, encoding='ascii'), bytes(access_key, encoding='ascii'), bytes(secret_key, encoding='ascii'))

        os.chdir(cur_path)

    def send_msg(self, topic: str, tag: str, key: str, msg: str, deliver_time_ms: int = 0):
        '''生产消息'''
        rst = self.h.ProducerSendMsg(self.producer, bytes(topic, encoding='ascii'), bytes(tag, encoding='ascii'), bytes(key, encoding='ascii'), bytes(msg, encoding='GBK'), deliver_time_ms)
        return rst.decode('GBK')

    def close(self):
        '''结束'''
        self.h.ProducerShutdown(self.producer)


class OrderProducer(object):
    '''生产者'''

    def __init__(self, pid: str, access_key: str, secret_key: str):
        '''初始化'''
        dlldir = os.path.abspath(os.path.dirname(__file__))
        cur_path = os.getcwd()
        os.chdir(dlldir)
        dlldir = os.path.join(dlldir, 'producer.' + ('dll' if 'Windows' in platform.system() else 'so'))
        self.h = CDLL(dlldir)

        self.h.OrderProducerStart.argtypes = [c_void_p, c_void_p, c_void_p]
        self.h.OrderProducerStart.restype = c_void_p

        self.h.OrderProducerShutdown.argtypes = [c_void_p]
        self.h.OrderProducerShutdown.restype = None

        self.h.OrderProducerSendMsg.argtypes = [c_void_p, c_void_p, c_void_p, c_void_p, c_void_p, c_void_p]
        self.h.OrderProducerSendMsg.restype = c_char_p

        self.producer = self.h.OrderProducerStart(bytes(pid, encoding='ascii'), bytes(access_key, encoding='ascii'), bytes(secret_key, encoding='ascii'))

        os.chdir(cur_path)

    def send_msg(self, topic: str, tag: str, key: str, msg: str, sharding_key: str):
        '''生产消息'''
        rst = self.h.OrderProducerSendMsg(self.producer, bytes(topic, encoding='ascii'), bytes(tag, encoding='ascii'), bytes(key, encoding='ascii'), bytes(msg, encoding='GBK'), bytes(sharding_key, encoding='ascii'))
        return rst.decode('GBK')

    def close(self):
        '''结束'''
        self.h.OrderProducerShutdown(self.producer)
