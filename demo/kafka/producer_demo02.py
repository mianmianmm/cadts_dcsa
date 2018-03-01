#!/usr/bin/python
# -*- coding:utf-8 -*-
import codecs

from pykafka import KafkaClient

client = KafkaClient(hosts="192.168.239.130:9092")

retopic=client.topics["retest1"]

refilename="auth.json"

def produce_kafka_file(filename,topic):
    with topic.get_sync_producer() as producer:
        with codecs.open(filename,"r") as rf:
            for line in rf:
                line = line.strip()
                if not line:
                    continue
                producer.produce(line)


produce_kafka_file(refilename,retopic)