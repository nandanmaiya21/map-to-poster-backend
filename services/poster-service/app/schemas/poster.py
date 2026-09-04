from typing import List, Optional

from pydantic import BaseModel


class Road(BaseModel):
    type: str
    coordinates: List[List[float]]


class PolygonFeature(BaseModel):
    coordinates: List[List[float]]


class MapData(BaseModel):
    roads: List[Road] = []
    water: List[PolygonFeature] = []
    parks: List[PolygonFeature] = []


class PosterRequest(BaseModel):
    map_id: str

    city: str = "Unknown"
    country: str = "Unknown"

    latitude: float
    longitude: float

    theme: str = "minimal"

    data: MapData