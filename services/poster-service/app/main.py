from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles

from app.clients.map_client import (
    get_map_data,
)

from app.renderers.poster_renderer import (
    render_poster,
)


app = FastAPI(
    title="Poster Service",
)


# =====================================
# SERVE GENERATED POSTERS
# =====================================

app.mount(
    "/exports",
    StaticFiles(directory="app/exports"),
    name="exports",
)


@app.get("/health")
def health():

    return {
        "status": "ok",
        "service": "poster-service",
    }


@app.post("/render/{map_id}")
async def render_map_poster(map_id: str):

    try:

        # Get processed geometry
        map_response = await get_map_data(
            map_id
        )

        # Check map status
        if map_response["status"] != "completed":

            return {
                "map_id": map_id,
                "status": map_response["status"],
                "message": "Map data is not ready yet",
            }

        map_data = map_response.get("data")

        if not map_data:
            raise HTTPException(
                status_code=400,
                detail="Map has no geometry data",
            )

        # =====================================
        # RENDER POSTER
        # =====================================

        output_path = render_poster(
            map_id=map_id,
            map_data=map_data,
        )

        filename = output_path.split("/")[-1]

        return {
            "status": "completed",
            "map_id": map_id,
            "file": filename,

            # Public URL
            "url": f"/exports/{filename}",

            "geometry": {
                "roads": len(
                    map_data.get("roads", [])
                ),
                "water": len(
                    map_data.get("water", [])
                ),
                "parks": len(
                    map_data.get("parks", [])
                ),
            },
        }

    except ValueError as error:

        raise HTTPException(
            status_code=404,
            detail=str(error),
        )

    except Exception as error:

        print(
            f"Poster render error: {error}",
            flush=True,
        )

        raise HTTPException(
            status_code=500,
            detail=str(error),
        )