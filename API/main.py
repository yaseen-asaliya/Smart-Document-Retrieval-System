from fastapi import FastAPI, Query
from query_processing import *
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow all origins for testing purposes; tighten this in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/search/")
async def search(query_param: str):
    return {"titles": ["t1", "t2","t3"]}

@app.get("/test/")
async def test():
    return "Done"

# In-memory data for demonstration purposes
fake_data = [
    {
        "id": i,
        "topics": ["topic1", "topic2"],
        "author": {"firstname": f"Author{i}", "surname": "LastName"},
        "temporal-expression": "2023-01-01",
        "geopoints": [{"lat": 40.7128 + i, "lon": -74.0060 + i} for i in range(1, 6)],
    }
    for i in range(1, 6)
]


@app.get("/query/")
async def search_articles(
    topics: str = Query(None, title="Topics", description="Comma-separated list of topics"),
    author: str = Query(None, title="Author", description="Author's name"),
    temporal_expression: str = Query(None, title="Temporal Expression", description="Temporal expression"),
    geopoint: str = Query(None, title="Geopoint", description="Latitude,Longitude"),
    page: int = Query(1, title="Page", description="Page number", ge=1),
    page_size: int = Query(10, title="Page Size", description="Number of items per page", le=100),
):
    # Filter the data based on the provided parameters
    filtered_data = fake_data
    if topics:
        filtered_data = [item for item in filtered_data if any(topic in item["topics"] for topic in topics.split(','))]
    if author:
        filtered_data = [item for item in filtered_data if author.lower() in f"{item['author']['firstname']} {item['author']['surname']}".lower()]
    if temporal_expression:
        filtered_data = [item for item in filtered_data if temporal_expression in item["temporal-expression"]]
    if geopoint:
        lat, lon = map(float, geopoint.split(','))
        filtered_data = [item for item in filtered_data if any(
            point["lat"] == lat and point["lon"] == lon for point in item["geopoints"]
        )]

    # Calculate pagination limits
    start_index = (page - 1) * page_size
    end_index = start_index + page_size

    # Return paginated data with "title" and "body"
    return {
        "data": [{"title": item["title"], "body": item["body"]} for item in filtered_data[start_index:end_index]],
        "total_items": len(filtered_data),
    }

