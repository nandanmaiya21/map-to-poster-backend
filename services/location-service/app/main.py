from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from geopy.exc import GeocoderServiceError, GeocoderTimedOut


app = FastAPI(title="Location Service")


# Nominatim's usage policy caps free public requests at ~1/sec and
# requires an identifying user agent - both matter here since this
# is called on every map-service /generate request.
_geolocator = Nominatim(user_agent="map-to-poster-backend")

_geocode = RateLimiter(_geolocator.geocode, min_delay_seconds=1)
_reverse = RateLimiter(_geolocator.reverse, min_delay_seconds=1)


class LocationResponse(BaseModel):
    name: str
    latitude: float
    longitude: float


class ReverseLocationResponse(BaseModel):
    # "place" is a query string osmnx's geocode_to_gdf/graph_from_place
    # can resolve directly, e.g. "Brantford, Ontario, Canada".
    place: str
    display_name: str
    latitude: float
    longitude: float


@app.get("/search", response_model=LocationResponse)
def search_location(q: str):

    try:
        location = _geocode(q, timeout=10)

    except (GeocoderServiceError, GeocoderTimedOut) as error:
        raise HTTPException(
            status_code=502,
            detail=f"Geocoding service failed: {error}",
        )

    if not location:
        raise HTTPException(
            status_code=404,
            detail=f"Location '{q}' not found",
        )

    return {
        "name": location.address,
        "latitude": location.latitude,
        "longitude": location.longitude,
    }


@app.get("/reverse", response_model=ReverseLocationResponse)
def reverse_location(lat: float, lon: float):

    try:
        location = _reverse(
            (lat, lon),
            timeout=10,
            addressdetails=True,
            # Without this, Nominatim defaults to building-level
            # precision (zoom=18) and resolves to whatever hamlet/
            # village/suburb contains the exact point, not the city
            # around it (e.g. a point in Udupi resolving to the
            # small village "Avarse" instead of "Udupi"). zoom=10
            # asks it to resolve at city level instead.
            zoom=10,
        )

    except (GeocoderServiceError, GeocoderTimedOut) as error:
        raise HTTPException(
            status_code=502,
            detail=f"Reverse geocoding service failed: {error}",
        )

    if not location:
        raise HTTPException(
            status_code=404,
            detail="No location found for these coordinates",
        )

    address = location.raw.get("address", {})

    city = (
        address.get("city")
        or address.get("town")
        or address.get("village")
        or address.get("municipality")
        or address.get("county")
    )

    if not city:
        raise HTTPException(
            status_code=404,
            detail="Could not determine a city for these coordinates",
        )

    state = address.get("state")
    country = address.get("country")

    place = ", ".join(
        part for part in (city, state, country) if part
    )

    return {
        "place": place,
        "display_name": location.address,
        "latitude": lat,
        "longitude": lon,
    }


@app.get("/health")
def health():
    return {"status": "ok"}
