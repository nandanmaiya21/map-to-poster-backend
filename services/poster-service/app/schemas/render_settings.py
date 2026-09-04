from dataclasses import dataclass


@dataclass
class RenderSettings:

    # Poster
    width: int
    height: int
    dpi: int

    # Map Camera
    map_padding: float
    map_coverage: float
    map_offset_x: float
    map_offset_y: float

    # Typography
    title_size: int | None
    subtitle_size: int | None
    coordinates_size: int | None
    font_weight: str

    # Gradients
    show_top_gradient: bool
    show_bottom_gradient: bool
    gradient_height: float
    gradient_strength: float

    # Divider
    show_divider: bool
    divider_width: float

    # Display
    show_title: bool
    show_subtitle: bool
    show_coordinates: bool
    show_attribution: bool

    # Layout
    layout: str