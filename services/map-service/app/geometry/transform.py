from app.geometry.projection import project_coordinates
from app.geometry.normalize import (
    get_bounds,
    normalize_coordinates,
)


def project_map_data(map_data):

    projected = {
        "roads": [],
        "water": [],
        "parks": [],
    }

    # Roads
    for road in map_data["roads"]:

        projected["roads"].append({
            "type": road["type"],
            "coordinates": project_coordinates(
                road["coordinates"]
            ),
        })

    # Water
    for feature in map_data["water"]:

        projected["water"].append({
            "coordinates": project_coordinates(
                feature["coordinates"]
            )
        })

    # Parks
    for feature in map_data["parks"]:

        projected["parks"].append({
            "coordinates": project_coordinates(
                feature["coordinates"]
            )
        })

    return projected


def normalize_map_data(
    map_data,
    width=1000,
    height=1000,
    padding=50,
):


    total_features = (
        len(map_data["roads"])
        + len(map_data["water"])
        + len(map_data["parks"])
    )

    if total_features == 0:
        raise ValueError("No map geometry available")

    bounds = get_bounds(map_data)

    normalized = {
        "roads": [],
        "water": [],
        "parks": [],
    }

    # Roads
    for road in map_data["roads"]:

        normalized["roads"].append({
            "type": road["type"],
            "coordinates": normalize_coordinates(
                road["coordinates"],
                bounds,
                width,
                height,
                padding,
            ),
        })

    # Water
    for feature in map_data["water"]:

        normalized["water"].append({
            "coordinates": normalize_coordinates(
                feature["coordinates"],
                bounds,
                width,
                height,
                padding,
            )
        })

    # Parks
    for feature in map_data["parks"]:

        normalized["parks"].append({
            "coordinates": normalize_coordinates(
                feature["coordinates"],
                bounds,
                width,
                height,
                padding,
            )
        })

    return normalized