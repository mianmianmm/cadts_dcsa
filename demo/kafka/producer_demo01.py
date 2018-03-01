#!/usr/bin/python
# -*- coding:utf-8 -*-

from pykafka import KafkaClient

client = KafkaClient(hosts="127.0.0.1:9092")
# 查看所有的topic
#print client.topics
topic = client.topics['testkafkamessage']


with topic.get_sync_producer() as producer:
    for i in range(4):
        producer.produce('test message'+ str(i))


