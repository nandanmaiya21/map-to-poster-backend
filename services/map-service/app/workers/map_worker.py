import json
import time

from app.database import SessionLocal
from app.models.map import Map
from app.queue import redis_client

from app.osm.client import (
    fetch_street_network,
    fetch_water_features,
    fetch_park_features,
)

from app.geometry.processor import process_map_data

from app.cache.map_cache import (
    get_cached_map,
    save_map_to_cache,
)


def update_map_status(
    map_id,
    status,
    data=None,
    error=None,
):
    """
    Update the map record in PostgreSQL.
    """

    db = SessionLocal()

    try:

        map_record = (
            db.query(Map)
            .filter(Map.id == map_id)
            .first()
        )

        if not map_record:

            print(
                f"⚠ Map record {map_id} not found",
                flush=True,
            )

            return

        map_record.status = status

        if data is not None:
            map_record.data = data
            map_record.error = None

        if error is not None:
            map_record.error = str(error)

        db.commit()

        print(
            f"✓ Database updated: {status}",
            flush=True,
        )

    except Exception as db_error:

        db.rollback()

        print(
            f"✗ Database update failed: {db_error}",
            flush=True,
        )

        raise

    finally:

        db.close()


def process_job(job):

    map_id = job["map_id"]

    attempt = job.get(
        "attempt",
        0,
    )

    max_attempts = job.get(
        "max_attempts",
        3,
    )

    print("\n" + "=" * 60)
    print("PROCESSING MAP JOB")
    print(f"Map ID: {map_id}")
    print(
        f"Attempt: {attempt + 1}/{max_attempts}"
    )
    print("=" * 60)

    try:

        latitude = job["latitude"]
        longitude = job["longitude"]
        distance = job["radius"]

        # ==================================
        # 0. CHECK PROCESSED MAP CACHE
        # ==================================

        print(
            "\n[0/4] CHECKING MAP CACHE",
            flush=True,
        )

        cached_map = get_cached_map(
            latitude,
            longitude,
            distance,
        )

        if cached_map is not None:

            print(
                "⚡ Using cached processed geometry",
                flush=True,
            )

            update_map_status(
                map_id=map_id,
                status="completed",
                data=cached_map,
            )

            redis_client.hset(
                f"map_status:{map_id}",
                mapping={
                    "status": "completed",
                    "cached": "true",
                },
            )

            print(
                f"\n✓ MAP {map_id} COMPLETED (CACHE)",
                flush=True,
            )

            return cached_map

        # ==================================
        # 1. STREETS
        # ==================================

        print(
            "\n[1/4] STREETS",
            flush=True,
        )

        graph = fetch_street_network(
            latitude,
            longitude,
            distance,
        )

        if graph is None:

            raise RuntimeError(
                "Street network unavailable"
            )

        # ==================================
        # 2. WATER
        # ==================================

        print(
            "\n[2/4] WATER",
            flush=True,
        )

        try:

            water = fetch_water_features(
                latitude,
                longitude,
                distance,
            )

        except Exception as error:

            print(
                f"⚠ Water unavailable: {error}",
                flush=True,
            )

            water = None

        # ==================================
        # 3. PARKS
        # ==================================

        print(
            "\n[3/4] PARKS",
            flush=True,
        )

        try:

            parks = fetch_park_features(
                latitude,
                longitude,
                distance,
            )

        except Exception as error:

            print(
                f"⚠ Parks unavailable: {error}",
                flush=True,
            )

            parks = None

        # ==================================
        # 4. PROCESS GEOMETRY
        # ==================================

        print(
            "\n[4/4] PROCESSING GEOMETRY",
            flush=True,
        )

        processed_data = process_map_data(
            graph,
            water,
            parks,
        )

        # ==================================
        # CACHE PROCESSED GEOMETRY
        # ==================================

        print(
            "\n💾 CACHING MAP GEOMETRY",
            flush=True,
        )

        save_map_to_cache(
            latitude,
            longitude,
            distance,
            processed_data,
        )

        # ==================================
        # SAVE TO POSTGRESQL
        # ==================================

        print(
            "\n💾 SAVING MAP DATA",
            flush=True,
        )

        update_map_status(
            map_id=map_id,
            status="completed",
            data=processed_data,
        )

        # ==================================
        # UPDATE REDIS STATUS
        # ==================================

        redis_client.hset(
            f"map_status:{map_id}",
            mapping={
                "status": "completed",
                "cached": "false",
            },
        )

        print(
            f"\n✓ MAP {map_id} COMPLETED",
            flush=True,
        )

        return processed_data

    except Exception as error:

        print(
            f"\n✗ JOB FAILED: {error}",
            flush=True,
        )

        # ==================================
        # RETRY
        # ==================================

        if attempt < max_attempts - 1:

            job["attempt"] = attempt + 1

            delay = RETRY_DELAY(
                job["attempt"]
            )

            print(
                f"⏳ Retrying in {delay} seconds...",
                flush=True,
            )

            update_map_status(
                map_id=map_id,
                status="retrying",
            )

            redis_client.hset(
                f"map_status:{map_id}",
                mapping={
                    "status": "retrying",
                    "attempt": job["attempt"],
                },
            )

            time.sleep(delay)

            # Redis client uses decode_responses=True
            # So push string, NOT encoded bytes
            redis_client.lpush(
                "map_jobs",
                json.dumps(job),
            )

        else:

            # ==================================
            # FINAL FAILURE
            # ==================================

            update_map_status(
                map_id=map_id,
                status="failed",
                error=error,
            )

            redis_client.hset(
                f"map_status:{map_id}",
                mapping={
                    "status": "failed",
                    "error": str(error),
                },
            )

            print(
                f"❌ MAP {map_id} PERMANENTLY FAILED",
                flush=True,
            )


def RETRY_DELAY(attempt):

    delays = {
        1: 10,
        2: 30,
        3: 60,
    }

    return delays.get(
        attempt,
        60,
    )


def start_worker():

    print(
        "🚀 Map Worker started...",
        flush=True,
    )

    while True:

        try:

            result = redis_client.brpop(
                "map_jobs",
                timeout=0,
            )

            if result is None:
                continue

            _, job_data = result

            # Supports both Redis configurations
            if isinstance(job_data, bytes):
                job_data = job_data.decode("utf-8")

            job = json.loads(job_data)

            process_job(job)

        except Exception as error:

            print(
                f"Worker error: {error}",
                flush=True,
            )

            time.sleep(5)


if __name__ == "__main__":
    start_worker()