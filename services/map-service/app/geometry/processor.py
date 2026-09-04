from app.geometry.roads import extract_roads
from app.geometry.features import extract_polygons
from app.geometry.transform import (
    project_map_data,
    normalize_map_data,
)
from app.geometry.optimizer import optimize_roads


def process_map_data(
    graph,
    water=None,
    parks=None,
):

    raw_map_data = {
        "roads": extract_roads(graph),
        "water": extract_polygons(water),
        "parks": extract_polygons(parks),
    }

    print(
        f"Raw roads: {len(raw_map_data['roads'])}",
        flush=True,
    )

    # Optimize BEFORE projection
    raw_map_data["roads"] = optimize_roads(
        raw_map_data["roads"]
    )

    print(
        f"Optimized roads: {len(raw_map_data['roads'])}",
        flush=True,
    )

    projected_map_data = project_map_data(
        raw_map_data
    )

    normalized_map_data = normalize_map_data(
        projected_map_data,
        width=1000,
        height=1000,
        padding=50,
    )

    return normalized_map_data