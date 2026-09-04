from dataclasses import dataclass


@dataclass
class RenderSettings:

    width: int
    height: int
    dpi: int

    map_padding: float

    map_coverage: float

    show_title: bool
    show_subtitle: bool
    show_coordinates: bool
    show_attribution: bool

    layout: str