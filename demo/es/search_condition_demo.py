from elasticsearch import Elasticsearch
from datetime import datetime

es=Elasticsearch()

body={

    "query": {
        "bool": {
            "must": [
                {
                    "query_string": {
                        "default_field": "message",
                        "query": "dbus"
                    }
                }
            ],
            "must_not": [ ],
            "should": [ ]
        }
    },
    "from": 0,
    "size": 50,
    "sort": [ ],
    "aggs": { }

}

res=es.search(index='kafka_logstash-2017.10.23',doc_type='logs',body=body)
print(res)
