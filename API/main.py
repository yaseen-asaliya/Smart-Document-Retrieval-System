from fastapi import FastAPI

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

    