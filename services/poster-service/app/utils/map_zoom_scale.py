def calculate_zoom_scale(
    coverage: float,
) -> float:
    """
    Calculate road width scale based
    on map camera coverage.

    Smaller coverage = more zoomed in.
    """

    if coverage <= 0:
        coverage = 0.1

    zoom_scale = 1 / coverage

    # Prevent ridiculous road widths
    return min(
        max(
            zoom_scale,
            0.7,
        ),
        3.0,
    )