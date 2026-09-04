from dataclasses import dataclass


@dataclass
class TypographySettings:

    # Title
    title_size: float
    title_weight: str

    # Subtitle
    subtitle_size: float
    subtitle_weight: str

    # Coordinates
    coordinates_size: float
    coordinates_weight: str


def calculate_title_size(
    title: str,
    poster_width: int,
    poster_height: int,
) -> float:
    """
    Calculate responsive title size.

    Typography scales based on poster dimensions
    and shrinks for long city names.
    """

    # Base scale uses the smaller dimension
    base_dimension = min(
        poster_width,
        poster_height,
    )

    # Base title size proportional to poster
    base_size = base_dimension * 0.026

    title_length = len(title.strip())

    # =====================================
    # LONG TITLE ADJUSTMENT
    # =====================================

    if title_length <= 8:

        multiplier = 1.0

    elif title_length <= 12:

        multiplier = 0.90

    elif title_length <= 16:

        multiplier = 0.78

    elif title_length <= 22:

        multiplier = 0.65

    else:

        multiplier = 0.52

    title_size = base_size * multiplier

    # Prevent extreme sizes
    return max(
        18,
        min(title_size, 120),
    )


def get_typography(
    width: int,
    height: int,
    title: str,
    title_size_override: int | None = None,
    subtitle_size_override: int | None = None,
    coordinates_size_override: int | None = None,
    font_weight: str = "bold",
) -> TypographySettings:
    """
    Generate responsive typography settings
    for the poster.
    """

    base_dimension = min(
        width,
        height,
    )

    # =====================================
    # TITLE
    # =====================================

    if title_size_override:

        title_size = title_size_override

    else:

        title_size = calculate_title_size(
            title=title,
            poster_width=width,
            poster_height=height,
        )

    # =====================================
    # SUBTITLE
    # =====================================

    if subtitle_size_override:

        subtitle_size = subtitle_size_override

    else:

        subtitle_size = max(
            10,
            min(
                base_dimension * 0.010,
                48,
            ),
        )

    # =====================================
    # COORDINATES
    # =====================================

    if coordinates_size_override:

        coordinates_size = coordinates_size_override

    else:

        coordinates_size = max(
            8,
            min(
                base_dimension * 0.007,
                32,
            ),
        )

    return TypographySettings(

        title_size=title_size,
        title_weight=font_weight,

        subtitle_size=subtitle_size,
        subtitle_weight="normal",

        coordinates_size=coordinates_size,
        coordinates_weight="normal",
    )