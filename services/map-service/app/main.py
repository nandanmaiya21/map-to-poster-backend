from fastapi import FastAPI, HTTPException
from uuid import uuid4

from app.schemas import MapRequest
from app.queue import enqueue_map_job
from app.init_db import init_db

from app.database import SessionLocal
from app.models.map import Map


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

    map_id = str(uuid4())

    # Create database session
    db = SessionLocal()

    try:

        # 1. Create map record in PostgreSQL
        new_map = Map(
            id=map_id,
            status="processing",
            latitude=request.latitude,
            longitude=request.longitude,
            radius=request.radius,
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
            "attempt": 0,
            "max_attempts": 3,
        }

        # 3. Push ONCE to Redis
        enqueue_map_job(job)

        return {
            "map_id": map_id,
            "status": "processing",
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