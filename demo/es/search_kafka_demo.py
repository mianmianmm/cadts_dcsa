from elasticsearch import Elasticsearch

words="dbus"
indextest='kafka_logstash-2017.10.23'

def key_search(indexx,keywords):

    es=Elasticsearch()

    body={

        "query": {
            "bool": {
                "must": [
                    {
                        "query_string": {
                            "default_field": "message",
                            "query": keywords
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

    res=es.search(index=indexx,body=body)
    print(res)

key_search(indextest,words)




