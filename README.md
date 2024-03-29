## Smart Document Retrieval System

Smart document retrieval system, a powerful tool implemented using the FastAPI framework with Python. This system empowers users to tailor their searches based on specific criteria such as article location, author, and topic.

> Application interface

![image](https://github.com/yaseen-asaliya/Smart-Document-Retrieval-System/assets/59315877/5cc89f26-4cae-4963-90e7-a92f28c763d5)

### Key Features

- **Customized Searches:** Users can refine their searches by specifying the location of the article, the author, and the topic.
  
- **Result Retrieval:** The system retrieves results from Elasticsearch, ensuring they align with the user's specified criteria.

- **User-Friendly GUI:** A graphical user interface (GUI) is provided, complete with a search box, to offer an intuitive and personalized search experience.

* Visualizing the Structure of Stored Articles in Elasticsearch
```
article_1
{
  "date": "YYYY-MM-DD HH:mm:ss",
  "topics": ["topic1", "topic2", ...],
  "title": "Article Title",
  "author": [{"firstname": author1_firstname, "surname": author1_surname}, {"firstname": author2_firstname, "surname": author2_surname}, ...],
  "analized-body": ["term1", "term2", ...],
  "body": "Main text content of the article.",
  "temporal-expression": ["expression": "time1", "expression": "time2", ...],
  "geopoints": [{"lat": latitude1, "lot": longitude1}, {"lat": latitude2, "lot": longitude2}, ...],   
  "georeferences": [{"lat": latitude1, "lot": longitude1}, {"lat": latitude2, "lot": longitude2}, ...]
}
``` 
* Index Mapping and Setting 
```
index_mapping = {
    "mappings": {
        "properties": {
            "date": {"type": "date"},
            "topics": {"type": "keyword"},
            "title": {"type": "text", "analyzer": "autocomplete", "search_analyzer": "autocomplete_search"},
            "author": {
                "type": "nested",
                "properties": {
                    "firstname": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
                    "surname": {"type": "text", "fields": {"keyword": {"type": "keyword"}}}
                }
            },
            "analized-body": {"type": "text"},
            "body": {"type": "text"},
            "temporal-expression": {
                "type": "nested",
                "properties": {
                    "expression": {"type": "text"}
                }
            },
            "geopoints": {
                "type": "nested",
                "properties": {
                    "lon": {"type": "double"},
                    "lat": {"type": "double"}
                }
            },
            "georeferences": {
                "type": "nested",
                "properties": {
                    "lon": {"type": "double"},
                    "lat": {"type": "double"}
                }
            }
        }
    },
    "settings": {
        "analysis": {
            "analyzer": {
                "autocomplete": {
                    "tokenizer": "autocomplete",
                    "filter": ["lowercase"]
                },
                "autocomplete_search": {
                    "tokenizer": "lowercase"
                }
            },
            "tokenizer": {
                "autocomplete": {
                    "type": "edge_ngram",
                    "min_gram": 3,
                    "max_gram": 10,
                    "token_chars": ["letter", "digit"]
                }
            }
        }
    }
}

```
* Articles Dates Distribution 
> This image was generated using an API from the applications.

![image](https://raw.githubusercontent.com/yaseen-asaliya/Smart-Document-Retrieval-System/phase_%232/documents_distribution_plot.png)
