import math


def calculate_bounds(
    latitude: float,
    longitude: float,
    radius_meters: int
):

    earth_radius = 6378137

    lat_delta = (
        radius_meters / earth_radius
    ) * (180 / math.pi)

    lon_delta = (
        radius_meters
        / earth_radius
        * (180 / math.pi)
        / math.cos(math.radians(latitude))
    )

    south = latitude - lat_delta
    north = latitude + lat_delta
    west = longitude - lon_delta
    east = longitude + lon_delta

    return {
        "south": south,
        "west": west,
        "north": north,
        "east": east
    }