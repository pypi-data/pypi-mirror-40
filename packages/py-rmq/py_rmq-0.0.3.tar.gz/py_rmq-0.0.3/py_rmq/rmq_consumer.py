#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : HaiFeng
# @Email   : 24918700@qq.com
# @Time    : 2019/1/15
# @desc    : consumer test

import os
from ctypes import *
import platform

class Consumer(object):
    '''消费者'''

    def __init__(self, cid: str, access_key: str, secret_key: str):
        ''' 使用示例 https://gitee.com/haifengat/ali_rmq_api/blob/master/py_rmq/rmq_test.py

        :param cid: CID_xxx
        :param access_key: access key
        :param secret_key: secret key
        '''
        dlldir = os.path.abspath(os.path.dirname(__file__))
        cur_path = os.getcwd()
        os.chdir(dlldir)
        dlldir = os.path.join(dlldir, 'consumer.' + ('dll' if 'Windows' in platform.system() else 'so'))
        self.h = CDLL(dlldir)

        self.h.CreateConsumer.argtypes = [c_void_p, c_void_p, c_void_p]
        self.h.CreateConsumer.restype = c_void_p
        self.consumer = self.h.CreateConsumer(bytes(cid, encoding='ascii'), bytes(access_key, encoding='ascii'), bytes(secret_key, encoding='ascii'))

        self.h.CreateListener.argtypes = []
        self.h.CreateListener.restype = c_void_p
        self.listener = self.h.CreateListener()

        self.h.SetOnConsumer.argtypes = [c_void_p, c_void_p]
        self.h.SetOnConsumer.restype = None
        self.evOnConsumer = CFUNCTYPE(None, c_char_p, c_char_p, c_char_p, c_char_p, c_longlong, c_char_p, c_int32, c_longlong, c_longlong)(self._OnConsumer)
        self.h.SetOnConsumer(self.listener, self.evOnConsumer)

        self.h.Shutdown.argtypes = [c_void_p]
        self.h.Shutdown.restype = None

        self.h.Subscribe.argtypes = [c_void_p, c_void_p, c_void_p, c_void_p]
        self.h.Subscribe.restype = None

        os.chdir(cur_path)

    def OnConsumer(self, topic: str, tag: str, key: str, id: str, deliver_time: int, body: str, reconsume_times: int, store_time: int, offset: int):
        '''收到消息时调用'''
        print(f'topic:{topic},tag:{tag},key:{key},id:{id},delivertime:{deliver_time}, body:{body}, reconsumetimes:{reconsume_times}, storetime:{store_time}, offset:{offset}')

    def _OnConsumer(self, topic: str, tag: str, key: str, id: str, deliver_time: int, body: str, reconsume_times: int, store_time: int, offset: int):
        topic = topic.decode("GBK")
        tag = tag.decode("GBK")
        key = key.decode("GBK")
        id = id.decode("GBK")
        body = body.decode("GBK")
        deliver_time = int(deliver_time)
        store_time = int(store_time)
        self.OnConsumer(topic, tag, key, id, deliver_time, body, reconsume_times, store_time, offset)

    def subscribe(self, topic: str, tag: str):
        '''订阅'''
        self.h.Subscribe(self.consumer, self.listener, bytes(topic, encoding='ascii'), bytes(tag, encoding='ascii'))

    def close(self):
        '''关闭,必须调用'''
        self.h.Shutdown(self.consumer)


class OrderConsumer(object):
    '''序列消费者'''

    def __init__(self, cid: str, access_key: str, secret_key: str):
        '''初始化'''
        dlldir = os.path.abspath(os.path.dirname(__file__))
        cur_path = os.getcwd()
        os.chdir(dlldir)
        dlldir = os.path.join(dlldir, 'consumer.' + ('dll' if 'Windows' in platform.system() else 'so'))
        self.h = CDLL(dlldir)

        self.h.CreateOrderConsumer.argtypes = [c_void_p, c_void_p, c_void_p]
        self.h.CreateOrderConsumer.restype = c_void_p
        self.consumer = self.h.CreateOrderConsumer(bytes(cid, encoding='ascii'), bytes(access_key, encoding='ascii'), bytes(secret_key, encoding='ascii'))

        self.h.CreateOrderListener.argtypes = []
        self.h.CreateOrderListener.restype = c_void_p
        self.listener = self.h.CreateOrderListener()

        self.h.SetOnOrderConsumer.argtypes = [c_void_p, c_void_p]
        self.h.SetOnOrderConsumer.restype = None
        self.evOnConsumer = CFUNCTYPE(None, c_char_p, c_char_p, c_char_p, c_char_p, c_longlong, c_char_p, c_int32, c_longlong, c_longlong)(self._OnConsumer)
        self.h.SetOnOrderConsumer(self.listener, self.evOnConsumer)

        self.h.ShutdownOrder.argtypes = [c_void_p]
        self.h.ShutdownOrder.restype = None

        self.h.SubscribeOrder.argtypes = [c_void_p, c_void_p, c_void_p, c_void_p]
        self.h.SubscribeOrder.restype = None

        os.chdir(cur_path)

    def OnConsumer(self, topic: str, tag: str, key: str, id: str, deliver_time: int, body: str, reconsume_times: int, store_time: int, offset: int):
        '''收到消息时调用'''
        print(f'topic:{topic},tag:{tag},key:{key},id:{id},delivertime:{deliver_time}, body:{body}, reconsumetimes:{reconsume_times}, storetime:{store_time}, offset:{offset}')

    def _OnConsumer(self, topic: str, tag: str, key: str, id: str, deliver_time: int, body: str, reconsume_times: int, store_time: int, offset: int):
        topic = topic.decode("GBK")
        tag = tag.decode("GBK")
        key = key.decode("GBK")
        id = id.decode("GBK")
        body = body.decode("GBK")
        deliver_time = int(deliver_time)
        store_time = int(store_time)
        self.OnConsumer(topic, tag, key, id, deliver_time, body, reconsume_times, store_time, offset)

    def subscribe(self, topic: str, tag: str):
        '''订阅'''
        self.h.SubscribeOrder(self.consumer, self.listener, bytes(topic, encoding='ascii'), bytes(tag, encoding='ascii'))

    def close(self):
        '''关闭,必须调用'''
        self.h.ShutdownOrder(self.consumer)
