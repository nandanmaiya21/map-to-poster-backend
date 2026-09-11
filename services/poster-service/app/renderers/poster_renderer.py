import hashlib
import os
from dataclasses import asdict

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

from matplotlib.collections import (
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

from app.typography.typography_engine import (
    get_typography,
)

from app.renderers.road_renderer import (
    render_roads,
)

from app.utils.map_zoom_scale import (
    calculate_zoom_scale,
)
from app.services.export_engine import (
    export_poster,
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
    Render MapToPoster-style poster.

    Pipeline:

    Map Data
        ↓
    Map Bounds
        ↓
    Map Camera
        ↓
    Poster Layout
        ↓
    Typography Engine
        ↓
    Gradients
        ↓
    Final Poster
    """

    # =====================================
    # LOAD POSTER LAYOUT
    # =====================================

    layout = get_layout(
        settings.layout,
    )

    # =====================================
    # LOAD RESPONSIVE TYPOGRAPHY
    # =====================================

    typography = get_typography(
        width=settings.width,
        height=settings.height,
        title=title,

        title_size_override=settings.title_size,
        subtitle_size_override=settings.subtitle_size,
        coordinates_size_override=settings.coordinates_size,

        font_weight=settings.font_weight,
    )

    # =====================================
    # GET MAP DATA
    # =====================================

    roads = map_data.get(
        "roads",
        [],
    )

    water = map_data.get(
        "water",
        [],
    )

    parks = map_data.get(
        "parks",
        [],
    )

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
    # CREATE POSTER FIGURE
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
    #
    # Only responsible for rendering
    # geographic features.
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
    # CALCULATE MAP BOUNDS
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
    #
    # Controls:
    #
    # - Coverage / zoom
    # - Horizontal offset
    # - Vertical offset
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

    # Map coordinates use screen-style Y.
    # Invert Y to preserve orientation.

    map_ax.set_ylim(
        ymax,
        ymin,
    )

    map_ax.set_aspect(
        "equal",
        adjustable="datalim",
    )

    map_ax.margins(
        0
    )

    map_ax.axis(
        "off"
    )


    # =====================================
    # POSTER OVERLAY AXIS
    #
    # Responsible for:
    #
    # - Gradients
    # - Typography
    # - Divider
    # - Attribution
    #
    # Coordinates are relative to the
    # entire poster canvas.
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


    zoom_scale = calculate_zoom_scale(
    settings.map_coverage)

    # =====================================
    # ROADS
    #
    # Includes:
    #
    # - hierarchy
    # - adaptive width
    # - opacity
    # - rounded joins
    # - road casing
    # =====================================

    render_roads(

        ax=map_ax,

        roads=roads,

        theme=theme,

        zoom_scale=zoom_scale,
    )



    # =====================================
    # BOTTOM GRADIENT
    #
    # Render before typography.
    # =====================================

    if settings.show_bottom_gradient:

        gradient_height = (
            settings.gradient_height
        )

        gradient_strength = (
            settings.gradient_strength
        )

        alpha = np.linspace(
            gradient_strength,
            0.0,
            500,
        ) ** 2.5

        gradient = np.zeros(
            (
                500,
                1,
                4,
            )
        )

        bg_color = matplotlib.colors.to_rgba(
            theme.background
        )

        gradient[:, 0, 0] = bg_color[0]
        gradient[:, 0, 1] = bg_color[1]
        gradient[:, 0, 2] = bg_color[2]
        gradient[:, 0, 3] = alpha

        poster_ax.imshow(

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
    # TOP GRADIENT
    # =====================================

    if settings.show_top_gradient:

        gradient_height = (
            settings.gradient_height
        )

        gradient_strength = (
            settings.gradient_strength
        )

        alpha = np.linspace(
            0.0,
            gradient_strength,
            500,
        ) ** 2.5

        gradient = np.zeros(
            (
                500,
                1,
                4,
            )
        )

        bg_color = matplotlib.colors.to_rgba(
            theme.background
        )

        gradient[:, 0, 0] = bg_color[0]
        gradient[:, 0, 1] = bg_color[1]
        gradient[:, 0, 2] = bg_color[2]
        gradient[:, 0, 3] = alpha

        poster_ax.imshow(

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
    # DIVIDER
    # =====================================

    if settings.show_divider:

        divider_half_width = (
            settings.divider_width / 2
        )

        poster_ax.plot(

            [
                0.5 - divider_half_width,
                0.5 + divider_half_width,
            ],

            [
                layout.divider_y,
                layout.divider_y,
            ],

            transform=poster_ax.transAxes,

            color=theme.text_primary,

            linewidth=1.2,

            alpha=0.9,

            zorder=30,
        )

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

            fontsize=typography.title_size,

            fontname=theme.font_family,

            fontweight=typography.title_weight,

            zorder=30,
        )

    # =====================================
    # SUBTITLE
    # =====================================

    if settings.show_subtitle and subtitle:

        poster_ax.text(

            0.5,

            layout.subtitle_y,

            subtitle.upper(),

            transform=poster_ax.transAxes,

            color=theme.text_primary,

            alpha=0.85,

            ha="center",

            va="center",

            fontsize=typography.subtitle_size,

            fontname=theme.font_family,

            fontweight=typography.subtitle_weight,

            zorder=30,
        )

    # =====================================
    # COORDINATES
    # =====================================

    if settings.show_coordinates and coordinates:

        poster_ax.text(

            0.5,

            layout.coordinates_y,

            coordinates,

            transform=poster_ax.transAxes,

            color=theme.text_secondary,

            alpha=0.8,

            ha="center",

            va="center",

            fontsize=typography.coordinates_size,

            fontname=theme.font_family,

            fontweight=typography.coordinates_weight,

            zorder=30,
        )

    # =====================================
    # ATTRIBUTION
    # =====================================

    if settings.show_attribution:

        poster_ax.text(

            0.98,

            0.02,

            "© OpenStreetMap contributors",

            transform=poster_ax.transAxes,

            color=theme.text_secondary,

            alpha=0.5,

            ha="right",

            va="bottom",

            fontsize=max(
                6,
                typography.coordinates_size * 0.5,
            ),

            fontname=theme.font_family,

            zorder=30,
        )

    # =====================================
    # OUTPUT PATH
    # =====================================

    theme_slug = (

        theme.slug

        if hasattr(
            theme,
            "slug",
        )

        else theme.name.lower().replace(
            " ",
            "-",
        )
    )

    output_path = os.path.join(

        EXPORT_DIR,

        f"{map_id}_{theme_slug}.png",
    )

   
    # =====================================
    # EXPORT
    # =====================================

    theme_slug = (
        theme.slug
        if hasattr(theme, "slug")
        else theme.name.lower().replace(
            " ",
            "-",
        )
    )

    # Distinguishes this render's output file/URL from any other
    # render of the same map+theme with different settings (layout,
    # coverage, offsets, gradients, text, ...) - see export_engine.
    render_signature = hashlib.sha256(
        repr(
            (
                asdict(settings),
                title,
                subtitle,
                coordinates,
            )
        ).encode("utf-8")
    ).hexdigest()[:10]

    output_path = export_poster(

        figure=figure,

        map_id=map_id,

        theme_slug=theme_slug,

        export_format=settings.export_format,

        dpi=settings.dpi,

        background_color=theme.background,

        render_signature=render_signature,
    )


    # =====================================
    # CLEANUP
    # =====================================

    plt.close(
        figure
    )


    print(
        f"✓ Poster exported: {output_path}",
        flush=True,
    )


    return output_path