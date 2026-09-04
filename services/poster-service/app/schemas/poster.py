from typing import Optional, Literal

from pydantic import BaseModel


class PosterRenderRequest(BaseModel):

    # =====================================
    # THEME
    # =====================================

    theme: str


    # =====================================
    # TEXT
    # =====================================

    title: str = "UNKNOWN"
    subtitle: str = ""
    coordinates: str = ""


    # =====================================
    # POSTER SIZE
    # =====================================

    width: Optional[int] = None
    height: Optional[int] = None
    dpi: Optional[int] = None


    # =====================================
    # MAP CAMERA
    # =====================================

    map_padding: float = 0.02

    map_coverage: float = 1.0

    map_offset_x: float = 0.0

    map_offset_y: float = 0.0


    # =====================================
    # TYPOGRAPHY
    # =====================================

    title_size: Optional[int] = None

    subtitle_size: Optional[int] = None

    coordinates_size: Optional[int] = None

    font_weight: str = "bold"


    # =====================================
    # GRADIENTS
    # =====================================

    show_top_gradient: bool = True

    show_bottom_gradient: bool = True

    gradient_height: float = 0.35

    gradient_strength: float = 1.0


    # =====================================
    # DIVIDER
    # =====================================

    show_divider: bool = True

    divider_width: float = 1.2


    # =====================================
    # DISPLAY OPTIONS
    # =====================================

    show_title: bool = True

    show_subtitle: bool = True

    show_coordinates: bool = True

    show_attribution: bool = True


    # =====================================
    # LAYOUT
    # =====================================

    layout: Literal[
        "full",
        "bottom",
        "center",
        "top",
    ] = "full"


    # =====================================
    # EXPORT
    # =====================================

    export_format: Literal[
        "png",
        "svg",
        "pdf",
    ] = "png"