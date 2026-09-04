import httpx


MAP_SERVICE_URL = "http://map-service:8000"


async def get_map_data(map_id: str):

    url = f"{MAP_SERVICE_URL}/maps/{map_id}"

    async with httpx.AsyncClient() as client:

        response = await client.get(
            url,
            timeout=30.0,
        )

    if response.status_code == 404:
        raise ValueError("Map not found")

    response.raise_for_status()

    return response.json()