def get_bounds(map_data):

    xs = []
    ys = []

    for category in ["roads", "water", "parks"]:

        for feature in map_data.get(category, []):

            for x, y in feature.get("coordinates", []):

                xs.append(x)
                ys.append(y)

    if not xs or not ys:
        raise ValueError(
            "Cannot normalize empty map data"
        )

    return {
        "min_x": min(xs),
        "max_x": max(xs),
        "min_y": min(ys),
        "max_y": max(ys),
    }


def get_normalization_config(
    bounds,
    width=1000,
    height=1000,
    padding=50,
):
    """
    Calculate one uniform scale factor.

    This preserves the geographic aspect ratio.
    """

    usable_width = width - (padding * 2)
    usable_height = height - (padding * 2)

    map_width = (
        bounds["max_x"] - bounds["min_x"]
    )

    map_height = (
        bounds["max_y"] - bounds["min_y"]
    )

    if map_width <= 0:
        map_width = 1

    if map_height <= 0:
        map_height = 1

    scale = min(
        usable_width / map_width,
        usable_height / map_height,
    )

    # Center the map
    scaled_width = map_width * scale
    scaled_height = map_height * scale

    offset_x = (
        (width - scaled_width) / 2
        - bounds["min_x"] * scale
    )

    offset_y = (
        (height - scaled_height) / 2
        + bounds["max_y"] * scale
    )

    return {
        "scale": scale,
        "offset_x": offset_x,
        "offset_y": offset_y,
    }


def normalize_coordinate(
    x,
    y,
    config,
):
    """
    Convert projected meters to poster coordinates.
    """

    normalized_x = (
        x * config["scale"]
        + config["offset_x"]
    )

    # Flip Y axis for canvas coordinates
    normalized_y = (
        -y * config["scale"]
        + config["offset_y"]
    )

    return [
        round(normalized_x, 2),
        round(normalized_y, 2),
    ]


def normalize_coordinates(
    coordinates,
    bounds,
    width=1000,
    height=1000,
    padding=50,
):
    """
    Normalize a list of coordinates.
    """

    config = get_normalization_config(
        bounds,
        width,
        height,
        padding,
    )

    return [
        normalize_coordinate(
            x,
            y,
            config,
        )
        for x, y in coordinates
    ]