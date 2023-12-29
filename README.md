## Smart Document Retrieval System

Smart document retrieval system, a powerful tool implemented using the FastAPI framework with Python. This system empowers users to tailor their searches based on specific criteria such as article location, author, and topic.

### Key Features

- **Customized Searches:** Users can refine their searches by specifying the location of the article, the author, and the topic.
  
- **Result Retrieval:** The system retrieves results from Elasticsearch, ensuring they align with the user's specified criteria.

- **User-Friendly GUI:** A graphical user interface (GUI) is provided, complete with a search box, to offer an intuitive and personalized search experience.

> Here is an example for the GUI

![image](https://github.com/yaseen-asaliya/Smart-Document-Retrieval-System/assets/59315877/5cc89f26-4cae-4963-90e7-a92f28c763d5)

* Articles Structure Visualisation on Elasticsearch
```
article
{
  "date": "YYYY-MM-DD HH:mm:ss",
  "topics": ["topic1", "topic2", ...],
  "title": "Article Title",
  "author": ["author1", "author2", ...],
  "analized-body": ["term1", "term2", ...],
  "body": "Main text content of the article.",
  "temporal-expression": ["time1", "time2", ...],
  "geopoints": [{"lat": latitude1, "lot": longitude1}, {"lat": latitude2, "lot": longitude2}, ...],   
  "georeferences": [{"lat": latitude1, "lot": longitude1}, {"lat": latitude2, "lot": longitude2}, ...]
}
``` 

* Articles Distribution 
> This image was generated using an API from the applications.

![image](https://raw.githubusercontent.com/yaseen-asaliya/Smart-Document-Retrieval-System/phase_%232/documents_distribution_plot.png)
