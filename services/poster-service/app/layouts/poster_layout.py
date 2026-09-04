from dataclasses import dataclass


@dataclass
class PosterLayout:

    # =====================================
    # MAP REGION
    #
    # Values are normalized (0.0 -> 1.0)
    # relative to the entire poster canvas.
    # =====================================

    map_left: float
    map_bottom: float
    map_width: float
    map_height: float


    # =====================================
    # TYPOGRAPHY
    #
    # Positions are relative to the FULL
    # poster canvas, not the map axis.
    # =====================================

    title_y: float
    subtitle_y: float
    coordinates_y: float


    # =====================================
    # DIVIDER
    #
    # Position relative to full poster.
    # =====================================

    divider_y: float


# =====================================
# FULL LAYOUT
#
# Map fills entire poster.
# Typography overlays bottom.
# =====================================

def create_full_layout():

    return PosterLayout(

        # Map
        map_left=0.0,
        map_bottom=0.0,
        map_width=1.0,
        map_height=1.0,

        # Typography
        title_y=0.14,
        subtitle_y=0.10,
        coordinates_y=0.07,

        # Divider
        divider_y=0.125,
    )


# =====================================
# BOTTOM TEXT LAYOUT
#
# Map occupies upper portion.
# Typography occupies bottom area.
# =====================================

def create_bottom_layout():

    return PosterLayout(

        # Map
        map_left=0.0,
        map_bottom=0.25,
        map_width=1.0,
        map_height=0.75,

        # Typography
        title_y=0.14,
        subtitle_y=0.10,
        coordinates_y=0.07,

        # Divider
        divider_y=0.19,
    )


# =====================================
# TOP TEXT LAYOUT
#
# Typography occupies top.
# Map occupies lower portion.
# =====================================

def create_top_layout():

    return PosterLayout(

        # Map
        map_left=0.0,
        map_bottom=0.0,
        map_width=1.0,
        map_height=0.75,

        # Typography
        title_y=0.90,
        subtitle_y=0.86,
        coordinates_y=0.82,

        # Divider
        divider_y=0.80,
    )


# =====================================
# CENTER MAP LAYOUT
#
# Map is framed inside poster.
# Typography occupies bottom.
# =====================================

def create_center_layout():

    return PosterLayout(

        # Map
        map_left=0.05,
        map_bottom=0.20,
        map_width=0.90,
        map_height=0.65,

        # Typography
        title_y=0.12,
        subtitle_y=0.075,
        coordinates_y=0.04,

        # Divider
        divider_y=0.16,
    )


# =====================================
# GET LAYOUT
# =====================================

def get_layout(
    layout_name: str,
) -> PosterLayout:

    layouts = {

        "full": create_full_layout,

        "bottom": create_bottom_layout,

        "top": create_top_layout,

        "center": create_center_layout,

    }

    layout_factory = layouts.get(
        layout_name,
    )

    if not layout_factory:

        raise ValueError(
            f"Unknown poster layout: {layout_name}"
        )

    return layout_factory()