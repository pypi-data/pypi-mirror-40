#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : HaiFeng
# @Email   : 24918700@qq.com
# @Time    : 2019/1/16
# @desc    : demo ali rocketmq

import sys
import time
from py_rmq.rmq_consumer import Consumer
from py_rmq.rmq_producer import Producer
from py_rmq.rmq_consumer import OrderConsumer
from py_rmq.rmq_producer import OrderProducer

def OnConsumer(topic: str, tag: str, key: str, id: str, deliver_time: int, body: str, reconsume_times: int, store_time: int, offset: int):
    print(body)


if __name__ == '__main__':

    t:str = ''
    id:str = ''
    access:str = ''
    secret:str = ''
    topic:str = ''

    if len(sys.argv) > 1:
        t = sys.argv[1].lower()
        if len(sys.argv) > 2:
            id = sys.argv[2]
            if len(sys.argv) > 3:
                access = sys.argv[3]
                if len(sys.argv) > 4:
                    secret = sys.argv[4]
                    if len(sys.argv) > 5:
                        topic = sys.argv[5]
    if t == '':
        t = input('select consumer or producer:').lower()
    if id == '':
        id = input('input cid or pid:')
    if access == '':
        access = input('input acces key:')
    if secret == '':
        secret = input('input secret key:')
    if topic == '':
        topic = input('input topic:')
    if t == 'consumer':
        print('test consumer...')
        c = Consumer(id, access, secret)
        c.OnConsumer = OnConsumer
        c.subscribe(topic, '*')
        input('press enter to continue test order consumer')
        c.close()

        print('test order consumer...')
        c = OrderConsumer(id, access, secret)
        c.OnConsumer = OnConsumer
        c.subscribe(topic, '*')
        input('press enter exit')
        c.close()
    else:
        tag = 'tag test'

        key = time.strftime('%Y%m%d%H%M%S', time.localtime())

        print('test producer...')
        p = Producer(id, access, secret)
        msg = input('input content: ')
        rst = p.send_msg(topic, tag, key, msg)
        print(f'result: {rst}')
        print('test delive msg, delive 30s')
        rst = p.send_msg(topic, tag, key, msg + 'delive', int(time.time() * 1000) + 30000)
        print(f'delive msg result: {rst}')
        p.close()

        input('press enter continue test order producer')
        p = OrderProducer(id, access, secret)
        sharding_key = input('input sharding_key: ')
        rst = p.send_msg(topic, tag, key, msg, sharding_key)
        print(f'order msg result: {rst}')
        p.close()