from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Location Service")


class LocationResponse(BaseModel):
    name: str
    latitude: float
    longitude: float


@app.get("/search", response_model=LocationResponse)
async def search_location(q: str):

    # Temporary mock
    if q.lower() == "toronto":
        return {
            "name": "Toronto",
            "latitude": 43.6532,
            "longitude": -79.3832
        }

    return {
        "name": q,
        "latitude": 0,
        "longitude": 0
    }


@app.get("/health")
async def health():
    return {"status": "ok"}