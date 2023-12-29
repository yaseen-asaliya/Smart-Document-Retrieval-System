from fastapi import FastAPI
from query_processing import *
import uvicorn
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configure CORS
origins = ["*"]  # Adjust this to your actual frontend origin(s)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

es = connect_to_elasticsearch()

class SearchRequest(BaseModel):
    query: str
    topic: str
    author: str
    specific_location: str

@app.post("/search/")
def search(request: SearchRequest):
    json_data = request.dict()
    return process_a_query(es, json_data["query"], json_data["topic"], extract_author(json_data["author"]), json_data["specific_location"])

@app.get("/top_ten/")
def get_top_ten():
    return get_top_10_georeferences(es)

@app.get("/dates_distribution/")
def get_distribution():
    return get_dates_distribution(es)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
