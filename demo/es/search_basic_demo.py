#coding=utf-8
from elasticsearch import Elasticsearch

es=Elasticsearch([{'host':'127.0.0.1','port':9200}])
index = "logstash-2017.10.17"
query={"query":{"match_all":{}}}
resp=es.search(index,body=query)
resp_docs=resp["hits"]["hits"]
total=resp["hits"]["total"]

print total
print resp_docs[0]['_source']['@timestamp']
