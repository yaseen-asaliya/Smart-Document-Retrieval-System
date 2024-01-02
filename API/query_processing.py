
from elasticsearch import Elasticsearch
from geopy.geocoders import Nominatim
import requests
import json
import spacy
import matplotlib.pyplot as plt

NUMBER_OF_DOCS_TO_RETRIVE = 10
FIRST_NAME = 0
SURNAME = 0
ELASTICSEARCH_PORT_NUMBER = 9200
ELASTICSEARCH_HOST = 'localhost'
DEFAULT_LON = 0
DEFAULT_LAT = 0
PLACE = 0
STATE = -1
COUNTRY = -2
DATE_LAST_DIGIT = 10
SKIP_ZERO_LON = 1
SKIP_ZERO_LAT = 1
INDEX_NAME = "smart_document_system"

def connect_to_elasticsearch():

    es = Elasticsearch([f'http://{ELASTICSEARCH_HOST}:{ELASTICSEARCH_PORT_NUMBER}'])
    
    if es.ping():
        print("Connected to Elasticsearch")
        return es
    else:
        print("Connection to Elasticsearch failed")


def get_coordinates(place):

    try:
        api_url = "https://nominatim.openstreetmap.org/search?format=json&q=" + place

        response = requests.get(api_url)
        data = json.loads(response.text)

        for item in data:
            if(item['addresstype'] == "city" or item['addresstype'] == "state" or item['addresstype'] == "country"):
                return {
                        "lat": item['lat'], 
                        "lon": item['lon']
                    }

    except Exception as e:
        print(f"Failed to retruive corrdinates: {e}")

    return {"lat": DEFAULT_LAT, "lon": DEFAULT_LON}


def extract_temporal_expressions(text, category):
    nlp = spacy.load("en_core_web_lg")
    doc = nlp(text)
    result = [ent.text for ent in doc.ents if ent.label_ == category]
    if len(result) >= 1:
        return result[0]
    return result


def get_device_location():
    response = requests.get('https://ipinfo.io')
    
    location_data = response.json()
    return location_data.get('city')

my_location = get_device_location()

def get_place_from_coordinates(latitude, longitude):
    geolocator = Nominatim(user_agent="smart-doc")
    location = geolocator.reverse((latitude, longitude), language='en')
    
    if location:
        return location.address
    else:
        return "Location not found"
    

def process_a_query(es, query, topic, author, specific_location):
    temporal_expression =  extract_temporal_expressions(query, "DATE")
    
    if specific_location:
        geopoint = get_coordinates(specific_location)
    else:
        geopoint = get_coordinates(my_location)

    query = {
        "query": {
            "bool": {
                "should": [
                    {
                        "match": {
                            "analized-body": {
                                "query": query
                                }
                            }
                        },
                    {
                        "match": {
                            "title": {
                                "query": query,
                                "boost": 3,
                            }
                        }
                    }
                ],
                "filter": []
            }
        }}

    if temporal_expression:
        query["query"]["bool"]["should"].append(
            {"nested": {
                "path": "temporal-expression",
                "query": {
                    "match": {
                        "temporal-expression.expression": {
                        "query": temporal_expression
                        }
                    }
                }
            }
        })
    
    if geopoint:
        type = ""
        if specific_location:
            type = "filter"
        else:
            type = "should"
            
        query["query"]["bool"][type].append(
            {
                "nested": {
                "path": "geopoints",
                "query": {
                        "bool": {
                        "must": [{ 
                            "match_all": {} },
                                { "term": { 
                                    "geopoints.lat": geopoint['lat'] 
                                    }},
                                { 
                                "term": { 
                                    "geopoints.lon": geopoint['lon'] 
                                    }}
                            ]
                        }   
                    }
                }
            })
       

    if topic:
        query["query"]["bool"]["filter"].append(
            {"match": {
                "topics": topic
                }
            }
        )

    if author:
        query["query"]["bool"]["filter"].append(
            {"nested": {
                "path": "author", 
                "query": {
                    "bool": {
                        "should": [
                            {"match": {
                                "author.firstname": author["firstname"]}
                            }, {
                                "match": {"author.surname": author["surname"]}}
                            ]
                        }
                    }
                }
            }
        )
    print(query)
    response = es.search(index=INDEX_NAME, body=query, size=NUMBER_OF_DOCS_TO_RETRIVE)

    results = []
    for hit in response["hits"]["hits"]:
        results.append({"title": hit["_source"]["title"]})

    unique_results = {tuple(d.items()) for d in results}

    final_results = [dict(t) for t in unique_results]

    return final_results

def extract_author(author_as_text):
    if author_as_text:
        tmp_author = author_as_text.split(" ")
        if len(tmp_author) == 1:
            return { "firstname": tmp_author[FIRST_NAME], "surname": "" }
        else:
            return { "firstname": tmp_author[FIRST_NAME], "surname": tmp_author[SURNAME] }
    else:
        return {}
    
def analyze_address(address):
    address = address.split(",")
    return  (address[PLACE] + "," + address[COUNTRY] + "," + address[STATE]).strip()
    
def get_top_10_georeferences(es):
    
    lon_aggs = {
        "terms": {
            "field": "georeferences.lon",
            "size": NUMBER_OF_DOCS_TO_RETRIVE
        }
    }
    
    lat_aggs = {
        "terms": {
            "field": "georeferences.lat",
            "size": NUMBER_OF_DOCS_TO_RETRIVE
        }
    }
    
    query = {
        "size": 0,
        "aggs": {
            "top_10_georeferences": {
            "nested": {
                "path": "georeferences"
            },
            "aggs": {
                "most_occurrence_latitudes": lat_aggs,
                "most_occurrence_longitudes": lon_aggs
                }
            }
        }
    }
    response = es.search(index=INDEX_NAME, body=query, size=NUMBER_OF_DOCS_TO_RETRIVE+1)
    
    places_names = []
    lon_path = response["aggregations"]["top_10_georeferences"]["most_occurrence_longitudes"]["buckets"]
    lat_path = response["aggregations"]["top_10_georeferences"]["most_occurrence_latitudes"]["buckets"]
    
    for lon_bucket, lat_bucket in zip(lon_path[SKIP_ZERO_LON:], lat_path[SKIP_ZERO_LAT:]):
        coords = get_place_from_coordinates(lat_bucket["key"], lon_bucket["key"])
        places_names.append(analyze_address(coords))
    
    return places_names

def get_dates_distribution(es):
    query = {
        "size": 0,
        "aggs": {
            "dates": {
                "date_histogram": {
                    "field": "date",
                    "calendar_interval": "day",
                    "min_doc_count": 1
                }
            }
        }
    }
    
    response = es.search(index=INDEX_NAME, body=query)

    dates = [article["key_as_string"][:DATE_LAST_DIGIT] for article in response["aggregations"]["dates"]["buckets"]]
    doc_counts = [article["doc_count"] for article in response["aggregations"]["dates"]["buckets"]]

    plt.figure(figsize=(10, 6))
    plt.bar(dates, doc_counts, color='blue')
    plt.xlabel('Date')
    plt.ylabel('Document Count')
    plt.title('Distribution of Documents Over Dates')
    plt.xticks(rotation=45, ha='right') 
    plt.tight_layout()
    
    plt.savefig('documents_distribution_plot.png')
    return "image saved successfully."
