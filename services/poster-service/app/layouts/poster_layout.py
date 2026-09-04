from dataclasses import dataclass


@dataclass
class PosterLayout:
    width: int
    height: int

    map_top: int
    map_bottom: int

    title_y: int
    subtitle_y: int
    coordinates_y: int


def create_portrait_layout(
    width=2000,
    height=3000,
):
    """
    Standard portrait poster layout.
    """

    map_top = 150

    # Map occupies approximately 75%
    map_bottom = int(height * 0.72)

    return PosterLayout(
        width=width,
        height=height,

        map_top=map_top,
        map_bottom=map_bottom,

        title_y=int(height * 0.82),
        subtitle_y=int(height * 0.87),
        coordinates_y=int(height * 0.93),
    )


def create_square_layout(
    size=2000,
):
    """
    Square poster layout.
    """

    return PosterLayout(
        width=size,
        height=size,

        map_top=100,
        map_bottom=int(size * 0.72),

        title_y=int(size * 0.80),
        subtitle_y=int(size * 0.86),
        coordinates_y=int(size * 0.93),
    )