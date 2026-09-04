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

from app.utils.map_camera import (
    apply_map_camera,
)
from app.layouts.poster_layout import (
    get_layout,
)
import numpy as np

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

    layout = get_layout(settings.layout,)

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
    # MAP AXIS
    # =====================================

    map_ax = figure.add_axes([
        layout.map_left,
        layout.map_bottom,
        layout.map_width,
        layout.map_height,
    ])

    map_ax.set_facecolor(
        theme.background
    )


    # =====================================
    # POSTER OVERLAY AXIS
    #
    # Used for typography and decorations
    # =====================================

    poster_ax = figure.add_axes([
        0,
        0,
        1,
        1,
    ])

    poster_ax.set_xlim(
        0,
        1,
    )

    poster_ax.set_ylim(
        0,
        1,
    )

    poster_ax.axis(
        "off"
    )

    map_ax.set_facecolor(
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

        map_ax.add_collection(
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

        map_ax.add_collection(
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

        map_ax.add_collection(
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
    # APPLY MAP CAMERA
    # =====================================

    xmin, xmax, ymin, ymax = apply_map_camera(

        xmin=xmin,
        xmax=xmax,

        ymin=ymin,
        ymax=ymax,

        coverage=settings.map_coverage,

        offset_x=settings.map_offset_x,

        offset_y=settings.map_offset_y,
    )
    # =====================================
    # APPLY MAP BOUNDS
    # =====================================

    map_ax.set_xlim(
        xmin,
        xmax,
    )

    # IMPORTANT:
    # Map coordinates use screen-style Y coordinates.
    # Smaller Y = visually higher.
    map_ax.set_ylim(
        ymax,
        ymin,
    )

    map_ax.set_aspect(
        "equal",
        adjustable="datalim",
    )

    map_ax.margins(0)

    map_ax.axis("off")


    # =====================================
    # POSTER OVERLAY AXIS
    # =====================================

    overlay_ax = figure.add_axes([
        0,
        0,
        1,
        1,
    ])

    overlay_ax.set_xlim(0, 1)
    overlay_ax.set_ylim(0, 1)

    overlay_ax.axis("off")

    # =====================================
    # DIVIDER LINE
    # =====================================

    if settings.show_divider:

        poster_ax.plot(
            [0.40, 0.60],

            [
                layout.divider_y,
                layout.divider_y,
            ],

            color=theme.text_primary,

            linewidth=settings.divider_width,

            alpha=0.9,

            zorder=30,
        )

    

    # =====================================
    # TITLE SIZE
    # =====================================

    if settings.title_size:

        title_size = settings.title_size

    else:

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

        poster_ax.text(
            0.5,
            layout.title_y,
            title.upper(),

            transform=poster_ax.transAxes,

            color=theme.text_primary,

            ha="center",
            va="center",

            fontsize=title_size,

            fontname=theme.font_family,

            fontweight=settings.font_weight,

            zorder=30,
        )
    # =====================================
    # COUNTRY / SUBTITLE
    # =====================================

    if settings.show_subtitle and subtitle:
        subtitle_size = (
        settings.subtitle_size
        if settings.subtitle_size
        else 18)

        poster_ax.text(
            0.5,
            layout.subtitle_y,
            subtitle.upper(),
            color=theme.text_primary,
            alpha=0.85,
            ha="center",
            va="center",
            fontsize=subtitle_size,
            fontname=theme.font_family,
            zorder=20,
        )

    # =====================================
    # COORDINATES
    # =====================================

    if settings.show_coordinates and coordinates:

        coordinates_size = (
        settings.coordinates_size
        if settings.coordinates_size
        else 13)

        poster_ax.text(
            0.5,
            layout.coordinates_y,
            coordinates,
            color=theme.text_secondary,
            alpha=0.8,
            ha="center",
            va="center",
            fontsize=coordinates_size,
            fontname=theme.font_family,
            zorder=20,
        )

    # =====================================
    # ATTRIBUTION
    # =====================================


    if settings.show_attribution:
        poster_ax.text(
            0.98,
            0.02,

            "© OpenStreetMap contributors",

            color=theme.text_secondary,

            alpha=0.5,

            ha="right",
            va="bottom",

            fontsize=7,

            fontname=theme.font_family,

            zorder=20,
        )

    # =====================================
    # BOTTOM TYPOGRAPHY GRADIENT
    # =====================================

    gradient_height = settings.gradient_height
    gradient_strength = settings.gradient_strength


    if settings.show_bottom_gradient:

        alpha = np.linspace(
            gradient_strength,
            0.0,
            500,
        ) ** 2.5

        gradient = np.zeros(
            (500, 1, 4)
        )

        bg_color = matplotlib.colors.to_rgba(
            theme.background
        )

        gradient[:, 0, 0] = bg_color[0]
        gradient[:, 0, 1] = bg_color[1]
        gradient[:, 0, 2] = bg_color[2]
        gradient[:, 0, 3] = alpha

        overlay_ax.imshow(
            gradient,

            extent=(
                0,
                1,
                0,
                gradient_height,
            ),

            origin="lower",

            aspect="auto",

            zorder=10,
        )
    # =====================================
    # TOP MAP GRADIENT
    # =====================================


    if settings.show_top_gradient:

        alpha = np.linspace(
            0.0,
            gradient_strength,
            500,
        ) ** 2.5

        gradient = np.zeros(
            (500, 1, 4)
        )

        bg_color = matplotlib.colors.to_rgba(
            theme.background
        )

        gradient[:, 0, 0] = bg_color[0]
        gradient[:, 0, 1] = bg_color[1]
        gradient[:, 0, 2] = bg_color[2]
        gradient[:, 0, 3] = alpha

        overlay_ax.imshow(
            gradient,

            extent=(
                0,
                1,
                1 - gradient_height,
                1,
            ),

            origin="lower",

            aspect="auto",

            zorder=10,
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