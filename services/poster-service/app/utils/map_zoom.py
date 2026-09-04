def apply_map_coverage(
    xmin: float,
    xmax: float,
    ymin: float,
    ymax: float,
    coverage: float,
):
    """
    Adjust map bounds based on coverage.

    coverage < 1.0 = zoom in
    coverage > 1.0 = zoom out
    coverage = 1.0 = unchanged
    """

    if coverage <= 0:
        raise ValueError(
            "map_coverage must be greater than 0"
        )

    # Calculate center
    center_x = (xmin + xmax) / 2
    center_y = (ymin + ymax) / 2

    # Current dimensions
    width = xmax - xmin
    height = ymax - ymin

    # Apply coverage
    new_width = width * coverage
    new_height = height * coverage

    # Rebuild bounds around center
    new_xmin = center_x - (new_width / 2)
    new_xmax = center_x + (new_width / 2)

    new_ymin = center_y - (new_height / 2)
    new_ymax = center_y + (new_height / 2)

    return (
        new_xmin,
        new_xmax,
        new_ymin,
        new_ymax,
    )