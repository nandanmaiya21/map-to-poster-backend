from matplotlib.collections import (
    LineCollection,
)

from app.styles.road_style import (
    get_road_style,
)


ROAD_DRAW_ORDER = [

    "default",

    "unclassified",

    "residential",

    "tertiary",

    "secondary",

    "primary",

    "trunk",

    "motorway",
]


def render_roads(
    ax,
    roads,
    theme,
    zoom_scale: float = 1.0,
):
    """
    Render roads using the Road Styling Engine.
    """

    # =====================================
    # GROUP ROADS BY TYPE
    # =====================================

    roads_by_type = {}

    for road in roads:

        coordinates = road.get(
            "coordinates",
            [],
        )

        if len(coordinates) < 2:
            continue

        road_type = road.get(
            "type",
            "default",
        ).lower()

        roads_by_type.setdefault(
            road_type,
            [],
        ).append(
            coordinates
        )

    # =====================================
    # DRAW ROAD TYPES
    # =====================================

    for road_type in ROAD_DRAW_ORDER:

        road_lines = roads_by_type.get(
            road_type,
            [],
        )

        if not road_lines:
            continue

        # Get adaptive style
        style = get_road_style(
            road_type=road_type,
            theme=theme,
            zoom_scale=zoom_scale,
        )

        collection = LineCollection(

            road_lines,

            colors=style.color,

            linewidths=style.width,

            alpha=style.alpha,

            zorder=style.zorder,

            capstyle="round",

            joinstyle="round",
        )

        ax.add_collection(
            collection
        )