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


# ==========================================
# WHOLE-CITY CACHE (by place name)
#
# A full-city Overpass fetch is much heavier than a point+radius
# bbox fetch, so this guards against two concurrent requests for
# the same not-yet-generated city both hitting Overpass at once.
# Stores the boundary alongside the data, since a cache hit skips
# fetch_city_boundary too.
# ==========================================

def generate_place_cache_key(place_name):

    normalized = place_name.strip().lower()

    key_hash = hashlib.sha256(
        normalized.encode("utf-8")
    ).hexdigest()

    return f"map_geometry_place:{key_hash}"


def get_cached_place_map(place_name):
    """
    Retrieve processed map geometry + boundary WKT for a place.
    """

    cache_key = generate_place_cache_key(place_name)

    cached = redis_client.get(cache_key)

    if not cached:

        print(
            "○ Cache MISS [place geometry]",
            flush=True,
        )

        return None

    print(
        "✓ Cache HIT [place geometry]",
        flush=True,
    )

    if isinstance(cached, bytes):
        cached = cached.decode("utf-8")

    return json.loads(cached)


def save_place_map_to_cache(place_name, data, boundary_wkt):
    """
    Save processed geometry + boundary WKT for a place to Redis.
    """

    cache_key = generate_place_cache_key(place_name)

    redis_client.setex(
        cache_key,
        CACHE_TTL,
        json.dumps(
            {
                "data": data,
                "boundary_wkt": boundary_wkt,
            },
            separators=(",", ":"),
        ),
    )

    print(
        "💾 Processed place geometry cached",
        flush=True,
    )