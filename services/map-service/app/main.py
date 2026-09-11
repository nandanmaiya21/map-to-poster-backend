from fastapi import FastAPI, HTTPException
from sqlalchemy import func
from uuid import uuid4

from app.schemas import MapRequest
from app.queue import enqueue_map_job
from app.init_db import init_db

from app.database import SessionLocal
from app.models.map import Map
from app.geometry.boundary import build_map_boundary
from app.clients.location_client import reverse_geocode_city


app = FastAPI(
    title="Map Service"
)


@app.on_event("startup")
def startup():
    init_db()


@app.get("/health")
async def health():
    return {
        "status": "ok"
    }


@app.post("/generate")
async def generate_map(request: MapRequest):

    # Create database session
    db = SessionLocal()

    try:

        # 0. Does this GPS point already fall inside a map we've
        # generated before? Compare against the stored coverage
        # boundary via PostGIS, not against exact coordinates.
        existing_map = (
            db.query(Map)
            .filter(Map.status == "completed")
            .filter(Map.boundary.isnot(None))
            .filter(
                func.ST_Contains(
                    Map.boundary,
                    func.ST_SetSRID(
                        func.ST_MakePoint(
                            request.longitude,
                            request.latitude,
                        ),
                        4326,
                    ),
                )
            )
            .first()
        )

        if existing_map:

            return {
                "map_id": existing_map.id,
                "status": existing_map.status,
                "reused": True,
            }

        map_id = str(uuid4())

        # Resolve the point to a city so the worker can fetch the
        # whole city (clipped to its real boundary) instead of just
        # a radius bbox. Falls back to radius-based generation below
        # if this can't be resolved - reverse_geocode_city returns
        # None rather than raising in that case.
        place = await reverse_geocode_city(
            request.latitude,
            request.longitude,
        )

        # 1. Create map record in PostgreSQL
        #
        # boundary starts as the radius bbox as an immediate
        # safety net (so this map can already be matched by other
        # requests while the job is still processing); the worker
        # overwrites it with the real city boundary once a
        # place-based generation succeeds.
        new_map = Map(
            id=map_id,
            status="processing",
            latitude=request.latitude,
            longitude=request.longitude,
            radius=request.radius,
            boundary=build_map_boundary(
                request.latitude,
                request.longitude,
                request.radius,
            ),
        )

        db.add(new_map)
        db.commit()
        db.refresh(new_map)

        # 2. Create worker job
        job = {
            "map_id": map_id,
            "latitude": request.latitude,
            "longitude": request.longitude,
            "radius": request.radius,
            "place": place,
            "attempt": 0,
            "max_attempts": 3,
        }

        # 3. Push ONCE to Redis
        enqueue_map_job(job)

        return {
            "map_id": map_id,
            "status": "processing",
            "reused": False,
        }

    except Exception as error:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=str(error),
        )

    finally:

        db.close()


@app.get("/maps/{map_id}")
async def get_map(map_id: str):

    db = SessionLocal()

    try:

        map_record = (
            db.query(Map)
            .filter(Map.id == map_id)
            .first()
        )

        if not map_record:
            raise HTTPException(
                status_code=404,
                detail="Map not found",
            )

        return {
            "map_id": map_record.id,
            "status": map_record.status,
            "latitude": map_record.latitude,
            "longitude": map_record.longitude,
            "radius": map_record.radius,
            "data": map_record.data,
            "error": map_record.error,
        }

    finally:

        db.close()