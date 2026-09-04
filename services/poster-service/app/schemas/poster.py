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
    # MAP SETTINGS
    # =====================================

    map_padding: float = 0.02

    map_coverage: float = 1.0


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
        "bottom"
    ] = "full"