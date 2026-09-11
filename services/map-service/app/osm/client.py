import time
import osmnx as ox

from app.osm.endpoints import (
    OVERPASS_ENDPOINTS,
    RETRY_DELAYS,
)


# ==========================================
# OSMNX SETTINGS
# ==========================================

ox.settings.use_cache = True
ox.settings.requests_timeout = 45
ox.settings.overpass_rate_limit = False


def execute_with_fallback(
    operation,
    operation_name: str,
):
    """
    Try an OSM operation against multiple
    Overpass endpoints.
    """

    last_error = None

    for index, endpoint in enumerate(OVERPASS_ENDPOINTS):

        try:

            print(
                f"\n🌐 [{operation_name.upper()}] "
                f"Trying endpoint "
                f"{index + 1}/{len(OVERPASS_ENDPOINTS)}",
                flush=True,
            )

            print(
                f"   {endpoint}",
                flush=True,
            )

            ox.settings.overpass_url = endpoint

            result = operation()

            print(
                f"✓ {operation_name} downloaded",
                flush=True,
            )

            return result

        except Exception as error:

            last_error = error

            print(
                f"✗ Endpoint failed: {error}",
                flush=True,
            )

            if index < len(OVERPASS_ENDPOINTS) - 1:

                delay = RETRY_DELAYS[min(index, len(RETRY_DELAYS) - 1)]

                print(
                    f"⏳ Waiting {delay}s before fallback...",
                    flush=True,
                )

                time.sleep(delay)

    raise RuntimeError(
        f"All Overpass endpoints failed. "
        f"Last error: {last_error}"
    )


# ==========================================
# STREETS
# ==========================================

def fetch_street_network(
    latitude,
    longitude,
    distance,
):

    point = (
        latitude,
        longitude,
    )

    print(
        f"Downloading street network around {point}",
        flush=True,
    )

    def operation():

        return ox.graph_from_point(
            point,
            dist=distance,
            dist_type="bbox",
            network_type="all",
            truncate_by_edge=True,
        )

    return execute_with_fallback(
        operation,
        "street network",
    )


# ==========================================
# WATER
# ==========================================

def fetch_water_features(
    latitude,
    longitude,
    distance,
):

    point = (
        latitude,
        longitude,
    )

    print(
        "Downloading water features...",
        flush=True,
    )

    def operation():

        return ox.features_from_point(
            point,
            tags={
                "natural": "water",
                "waterway": True,
            },
            dist=distance,
        )

    return execute_with_fallback(
        operation,
        "water features",
    )


# ==========================================
# PARKS
# ==========================================

def fetch_park_features(
    latitude,
    longitude,
    distance,
):

    point = (
        latitude,
        longitude,
    )

    print(
        "Downloading park features...",
        flush=True,
    )

    def operation():

        return ox.features_from_point(
            point,
            tags={
                "leisure": "park",
            },
            dist=distance,
        )

    return execute_with_fallback(
        operation,
        "park features",
    )


# ==========================================
# WHOLE-CITY FETCH (by place name)
#
# Unlike the point+radius functions above,
# these clip to the real administrative
# boundary OSM has for the place, not a bbox.
# ==========================================

def fetch_city_boundary(place_name):
    """
    Returns a GeoDataFrame (one row) with the place's real
    administrative boundary polygon/multipolygon, via Nominatim -
    not an Overpass endpoint, so no endpoint fallback here.
    """

    print(
        f"Downloading city boundary for {place_name}",
        flush=True,
    )

    return ox.geocode_to_gdf(place_name)


def fetch_street_network_for_place(
    place_name,
):

    print(
        f"Downloading street network for {place_name}",
        flush=True,
    )

    def operation():

        return ox.graph_from_place(
            place_name,
            network_type="all",
            truncate_by_edge=True,
        )

    return execute_with_fallback(
        operation,
        "street network (place)",
    )


def fetch_water_features_for_place(
    place_name,
):

    print(
        f"Downloading water features for {place_name}",
        flush=True,
    )

    def operation():

        return ox.features_from_place(
            place_name,
            tags={
                "natural": "water",
                "waterway": True,
            },
        )

    return execute_with_fallback(
        operation,
        "water features (place)",
    )


def fetch_park_features_for_place(
    place_name,
):

    print(
        f"Downloading park features for {place_name}",
        flush=True,
    )

    def operation():

        return ox.features_from_place(
            place_name,
            tags={
                "leisure": "park",
            },
        )

    return execute_with_fallback(
        operation,
        "park features (place)",
    )