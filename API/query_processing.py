
from elasticsearch import Elasticsearch


index_name = "smart-document-system"


def connect_to_elasticsearch():
    elasticsearch_host = 'localhost'
    elasticsearch_port = 9200

    es = Elasticsearch([f'http://{elasticsearch_host}:{elasticsearch_port}'])
    
    if es.ping():
        print("Connected to Elasticsearch")
        return es
    else:
        print("Connection to Elasticsearch failed")
    
    
def process_a_query(query, temporal_expression, geopoint, topic, author):
    es = connect_to_elasticsearch()
    
    
    
    
    
    