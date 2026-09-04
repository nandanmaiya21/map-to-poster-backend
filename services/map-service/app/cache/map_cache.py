import json
import hashlib

from app.queue import redis_client


CACHE_TTL = 60 * 60 * 24 * 7  # 7 days


def generate_cache_key(
    latitude,
    longitude,
    radius,
):
    """
    Generate a stable cache key for a map location.
    """

    raw_key = (
        f"{round(latitude, 5)}:"
        f"{round(longitude, 5)}:"
        f"{radius}"
    )

    key_hash = hashlib.sha256(
        raw_key.encode("utf-8")
    ).hexdigest()

    return f"map_geometry:{key_hash}"


def get_cached_map(
    latitude,
    longitude,
    radius,
):
    """
    Retrieve processed map geometry from Redis.
    """

    cache_key = generate_cache_key(
        latitude,
        longitude,
        radius,
    )

    cached = redis_client.get(cache_key)

    if not cached:

        print(
            "○ Cache MISS [map geometry]",
            flush=True,
        )

        return None

    print(
        "✓ Cache HIT [map geometry]",
        flush=True,
    )

    if isinstance(cached, bytes):
        cached = cached.decode("utf-8")

    return json.loads(cached)


def save_map_to_cache(
    latitude,
    longitude,
    radius,
    data,
):
    """
    Save processed JSON-serializable geometry to Redis.
    """

    cache_key = generate_cache_key(
        latitude,
        longitude,
        radius,
    )

    redis_client.setex(
        cache_key,
        CACHE_TTL,
        json.dumps(
            data,
            separators=(",", ":"),
        ),
    )

    print(
        "💾 Processed map geometry cached",
        flush=True,
    )