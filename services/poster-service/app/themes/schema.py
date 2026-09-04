from dataclasses import dataclass
from typing import Dict


@dataclass
class Theme:

    name: str

    background: str

    water_color: str
    park_color: str

    road_colors: Dict[str, str]
    road_widths: Dict[str, float]

    text_primary: str
    text_secondary: str

    font_family: str

    width: int = 2000
    height: int = 3000
    dpi: int = 300