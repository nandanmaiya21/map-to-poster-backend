from dataclasses import dataclass


@dataclass
class RoadStyle:

    color: str
    width: float
    alpha: float
    zorder: int


ROAD_HIERARCHY = {

    "motorway": 8,

    "trunk": 7,

    "primary": 6,

    "secondary": 5,

    "tertiary": 4,

    "residential": 3,

    "unclassified": 2,

    "default": 1,
}


def get_road_style(
    road_type: str,
    theme,
    zoom_scale: float = 1.0,
) -> RoadStyle:
    """
    Resolve visual style for a road.

    zoom_scale controls how thick roads appear
    depending on the map camera zoom.
    """

    # Normalize road type
    road_type = road_type.lower()

    # -------------------------------------
    # COLOR
    # -------------------------------------

    color = theme.road_colors.get(
        road_type,
        theme.road_colors.get(
            "default",
            "#FFFFFF",
        ),
    )

    # -------------------------------------
    # BASE WIDTH
    # -------------------------------------

    base_width = theme.road_widths.get(
        road_type,
        theme.road_widths.get(
            "default",
            0.3,
        ),
    )

    # -------------------------------------
    # ROAD HIERARCHY
    # -------------------------------------

    hierarchy = ROAD_HIERARCHY.get(
        road_type,
        1,
    )

    # -------------------------------------
    # ZOOM ADAPTIVE WIDTH
    # -------------------------------------

    width = (
        base_width
        * zoom_scale
    )

    # -------------------------------------
    # OPACITY
    # -------------------------------------

    if hierarchy >= 6:

        alpha = 1.0

    elif hierarchy >= 4:

        alpha = 0.95

    else:

        alpha = 0.85

    # -------------------------------------
    # LAYER ORDER
    # -------------------------------------

    zorder = 5 + hierarchy

    return RoadStyle(
        color=color,
        width=width,
        alpha=alpha,
        zorder=zorder,
    )