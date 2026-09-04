import json
import os
from redis import Redis


REDIS_URL = os.getenv(
    "REDIS_URL",
    "redis://localhost:6379/0"
)


redis_client = Redis.from_url(
    REDIS_URL,

    # IMPORTANT:
    # Keep raw bytes because map cache uses pickle
    decode_responses=False,

    socket_connect_timeout=5,

    # No timeout while BRPOP blocks
    socket_timeout=None,

    socket_keepalive=True,
)


def enqueue_map_job(job: dict):
    redis_client.lpush(
        "map_jobs",
        json.dumps(job).encode("utf-8")
    )