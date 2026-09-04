from pydantic import BaseModel, Field


class MapRequest(BaseModel):
    latitude: float
    longitude: float

    radius: int = Field(
        default=3000,
        ge=500,
        le=10000
    )