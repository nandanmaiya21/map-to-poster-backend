import os
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt

from matplotlib.collections import (
    LineCollection,
    PolyCollection,
)
from app.utils.map_bounds import (
    calculate_map_bounds,
)
from app.utils.map_zoom import (
    apply_map_coverage,
)

EXPORT_DIR = "/app/app/exports"


def render_poster(
    map_id: str,
    map_data: dict,
    theme,
    settings,
    title: str = "UNKNOWN",
    subtitle: str = "",
    coordinates: str = "",
   
):
    """
    Render MapToPoster-style full canvas poster.
    """

    roads = map_data.get("roads", [])
    water = map_data.get("water", [])
    parks = map_data.get("parks", [])

    if not roads:
        raise ValueError(
            "No road data available"
        )

    # =====================================
    # CREATE EXPORT DIRECTORY
    # =====================================

    os.makedirs(
        EXPORT_DIR,
        exist_ok=True,
    )

    # =====================================
    # CREATE FULL POSTER FIGURE
    # =====================================

    figure = plt.figure(
        figsize=(
            settings.width / settings.dpi,
            settings.height / settings.dpi,
        ),
        dpi=settings.dpi,
        facecolor=theme.background,
    )

    # =====================================
    # SINGLE FULL-CANVAS AXIS
    # =====================================

    ax = figure.add_axes([
        0,
        0,
        1,
        1,
    ])

    ax.set_facecolor(
        theme.background
    )

    # =====================================
    # WATER
    # =====================================

    water_polygons = []

    for feature in water:

        coordinates_data = feature.get(
            "coordinates",
            [],
        )

        if len(coordinates_data) >= 3:

            water_polygons.append(
                coordinates_data
            )

    if water_polygons:

        water_collection = PolyCollection(
            water_polygons,
            facecolors=theme.water_color,
            edgecolors="none",
            alpha=1.0,
            zorder=1,
        )

        ax.add_collection(
            water_collection
        )

    # =====================================
    # PARKS
    # =====================================

    park_polygons = []

    for feature in parks:

        coordinates_data = feature.get(
            "coordinates",
            [],
        )

        if len(coordinates_data) >= 3:

            park_polygons.append(
                coordinates_data
            )

    if park_polygons:

        park_collection = PolyCollection(
            park_polygons,
            facecolors=theme.park_color,
            edgecolors="none",
            alpha=1.0,
            zorder=2,
        )

        ax.add_collection(
            park_collection
        )

    # =====================================
    # GROUP ROADS BY TYPE
    # =====================================

    roads_by_type = {}

    for road in roads:

        road_coordinates = road.get(
            "coordinates",
            [],
        )

        if len(road_coordinates) < 2:
            continue

        road_type = road.get(
            "type",
            "default",
        )

        roads_by_type.setdefault(
            road_type,
            [],
        ).append(
            road_coordinates
        )

    # =====================================
    # ROAD DRAWING ORDER
    #
    # Draw small roads first
    # Big roads last
    # =====================================

    road_order = [

        "default",

        "unclassified",

        "residential",

        "tertiary",

        "secondary",

        "primary",

        "trunk",

        "motorway",

    ]

    for road_type in road_order:

        road_lines = roads_by_type.get(
            road_type,
            [],
        )

        if not road_lines:
            continue

        color = theme.road_colors.get(
            road_type,
            theme.road_colors.get(
                "default",
                "#FFFFFF",
            ),
        )

        width = theme.road_widths.get(
            road_type,
            theme.road_widths.get(
                "default",
                0.3,
            ),
        )

        roads_collection = LineCollection(
            road_lines,
            colors=color,
            linewidths=width,
            alpha=0.95,
            zorder=5,
        )

        ax.add_collection(
            roads_collection
        )

    # =====================================
    # CALCULATE DYNAMIC MAP BOUNDS
    # =====================================

    xmin, xmax, ymin, ymax = calculate_map_bounds(
        roads=roads,
        water=water,
        parks=parks,
        poster_width=settings.width,
        poster_height=settings.height,
        padding=settings.map_padding,
    )

    # =====================================
    # APPLY USER MAP COVERAGE
    # =====================================

    xmin, xmax, ymin, ymax = apply_map_coverage(
    xmin=xmin,
    xmax=xmax,
    ymin=ymin,
    ymax=ymax,
    coverage=settings.map_coverage,
    )

    # =====================================
    # APPLY MAP BOUNDS
    # =====================================

    ax.set_xlim(
        xmin,
        xmax,
    )

    ax.set_ylim(
        ymax,
        ymin,
    )

    ax.set_aspect(
    "equal",
    adjustable="datalim",
    )

    ax.margins(0)

    ax.axis("off")


    print(
        "MAP BOUNDS:",
        xmin,
        xmax,
        ymin,
        ymax,
        flush=True,
    )



    # =====================================
    # DIVIDER LINE
    # =====================================

    ax.plot(
        [0.40, 0.60],
        [0.125, 0.125],
        transform=ax.transAxes,
        color=theme.text_primary,
        linewidth=1.2,
        alpha=0.9,
        zorder=20,
    )

    # =====================================
    # ADAPTIVE TITLE SIZE
    # =====================================

    base_title_size = 42

    title_length = len(title)

    if title_length > 10:

        scale = 10 / title_length

        title_size = max(
            base_title_size * scale,
            18,
        )

    else:

        title_size = base_title_size

    # =====================================
    # CITY TITLE
    # =====================================

    if settings.show_title and title:

        ax.text(
            0.5,
            0.14,
            title.upper(),
            transform=ax.transAxes,
            color=theme.text_primary,
            ha="center",
            va="center",
            fontsize=title_size,
            fontname=theme.font_family,
            fontweight="bold",
            zorder=20,
        )

    # =====================================
    # COUNTRY / SUBTITLE
    # =====================================

    if settings.show_subtitle and subtitle:

        ax.text(
            0.5,
            0.10,
            subtitle.upper(),
            transform=ax.transAxes,
            color=theme.text_primary,
            alpha=0.85,
            ha="center",
            va="center",
            fontsize=18,
            fontname=theme.font_family,
            zorder=20,
        )

    # =====================================
    # COORDINATES
    # =====================================

    if settings.show_coordinates and coordinates:

        ax.text(
            0.5,
            0.07,
            coordinates,
            transform=ax.transAxes,
            color=theme.text_secondary,
            alpha=0.8,
            ha="center",
            va="center",
            fontsize=13,
            fontname=theme.font_family,
            zorder=20,
        )

    # =====================================
    # ATTRIBUTION
    # =====================================


    if settings.show_attribution:
        ax.text(
            0.98,
            0.02,
            "© OpenStreetMap contributors",
            transform=ax.transAxes,
            color=theme.text_secondary,
            alpha=0.5,
            ha="right",
            va="bottom",
            fontsize=7,
            fontname=theme.font_family,
            zorder=20,
        )

    # =====================================
    # OUTPUT
    # =====================================

    theme_slug = (
        theme.slug
        if hasattr(theme, "slug")
        else theme.name.lower().replace(" ", "-")
    )

    output_path = os.path.join(
        EXPORT_DIR,
        f"{map_id}_{theme_slug}.png",
    )

    figure.savefig(
        output_path,
        dpi=settings.dpi,
        facecolor=theme.background,
        pad_inches=0,
    )

    plt.close(figure)

    print(
        f"✓ Poster saved: {output_path}",
        flush=True,
    )

    return output_path