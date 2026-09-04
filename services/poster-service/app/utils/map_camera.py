def apply_map_camera(
    xmin: float,
    xmax: float,
    ymin: float,
    ymax: float,
    coverage: float = 1.0,
    offset_x: float = 0.0,
    offset_y: float = 0.0,
):
    """
    Apply camera zoom and pan.

    coverage:
        Higher = zoom in / map occupies more screen

    offset_x:
        Positive = move map visually right

    offset_y:
        Positive = move map visually up
    """

    # =====================================
    # CALCULATE CENTER
    # =====================================

    center_x = (
        xmin + xmax
    ) / 2

    center_y = (
        ymin + ymax
    ) / 2


    # =====================================
    # CURRENT SIZE
    # =====================================

    width = xmax - xmin

    height = ymax - ymin


    # =====================================
    # ZOOM
    #
    # Higher coverage = tighter viewport
    # =====================================

    coverage = max(
        coverage,
        0.01,
    )

    new_width = (
        width / coverage
    )

    new_height = (
        height / coverage
    )


    # =====================================
    # PAN
    # =====================================

    center_x += (
        width * offset_x
    )

    center_y -= (
        height * offset_y
    )


    # =====================================
    # RETURN CAMERA VIEWPORT
    # =====================================

    return (
        center_x - new_width / 2,
        center_x + new_width / 2,
        center_y - new_height / 2,
        center_y + new_height / 2,
    )