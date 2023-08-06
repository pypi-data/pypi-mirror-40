from es import AggsNode
# from elasticsearch import Elasticsearch
# _es = Elasticsearch('localhost:9200')

a = AggsNode('a', size=10)
b = AggsNode('c', bucket='sum', size=10)
a.order = b.bucket
a.child_aggs = b

print(a.parse())