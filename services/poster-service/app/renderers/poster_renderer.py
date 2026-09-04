import os

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection


EXPORT_DIR = "/app/app/exports"


def render_poster(
    map_id: str,
    map_data: dict,
):
    """
    Render map roads into a PNG poster.
    """

    roads = map_data.get(
        "roads",
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
    # CREATE CANVAS
    # =====================================

    figure, axis = plt.subplots(
        figsize=(10, 10),
        dpi=150,
    )

    # Background
    background_color = "#111111"

    figure.patch.set_facecolor(
        background_color
    )

    axis.set_facecolor(
        background_color
    )

    # =====================================
    # PREPARE ROAD LINES
    # =====================================

    road_lines = []

    for road in roads:

        coordinates = road.get(
            "coordinates",
            [],
        )

        if len(coordinates) < 2:
            continue

        road_lines.append(
            coordinates
        )

    # =====================================
    # DRAW ROADS
    # =====================================

    roads_collection = LineCollection(
        road_lines,
        colors="#F2F2F2",
        linewidths=0.35,
        alpha=0.9,
    )

    axis.add_collection(
        roads_collection
    )

    # =====================================
    # CANVAS SETTINGS
    # =====================================

    axis.set_xlim(
        0,
        1000,
    )

    axis.set_ylim(
        1000,
        0,
    )

    axis.set_aspect(
        "equal"
    )

    axis.axis(
        "off"
    )

    # Remove margins
    plt.subplots_adjust(
        left=0,
        right=1,
        top=1,
        bottom=0,
    )

    # =====================================
    # SAVE PNG
    # =====================================

    output_path = os.path.join(
        EXPORT_DIR,
        f"{map_id}.png",
    )

    figure.savefig(
        output_path,
        dpi=300,
        facecolor=background_color,
        bbox_inches="tight",
        pad_inches=0,
    )

    plt.close(
        figure
    )

    print(
        f"✓ Poster saved: {output_path}",
        flush=True,
    )

    return output_path