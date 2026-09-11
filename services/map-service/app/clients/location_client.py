import os

import httpx


LOCATION_SERVICE_URL = os.getenv(
    "LOCATION_SERVICE_URL",
    "http://location-service:8000",
)


async def reverse_geocode_city(latitude: float, longitude: float):
    """
    Resolve a GPS point to a place name osmnx can fetch by
    (e.g. "Brantford, Ontario, Canada"). Returns None if the
    point can't be resolved to a city - callers should fall
    back to radius-based generation in that case.
    """

    url = f"{LOCATION_SERVICE_URL}/reverse"

    try:

        async with httpx.AsyncClient() as client:

            response = await client.get(
                url,
                params={
                    "lat": latitude,
                    "lon": longitude,
                },
                timeout=15.0,
            )

    except httpx.HTTPError:
        return None

    if response.status_code != 200:
        return None

    return response.json()["place"]
