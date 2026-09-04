from typing import Dict

from pydantic import BaseModel


class ThemeBase(BaseModel):

    slug: str

    name: str

    background: str

    water_color: str

    park_color: str

    road_colors: Dict[str, str]

    road_widths: Dict[str, float]

    text_primary: str

    text_secondary: str

    font_family: str = "DejaVu Sans"

    width: int = 2000

    height: int = 3000

    dpi: int = 300


class ThemeCreate(ThemeBase):
    pass


class ThemeUpdate(BaseModel):

    name: str | None = None

    background: str | None = None

    water_color: str | None = None

    park_color: str | None = None

    road_colors: Dict[str, str] | None = None

    road_widths: Dict[str, float] | None = None

    text_primary: str | None = None

    text_secondary: str | None = None

    font_family: str | None = None

    width: int | None = None

    height: int | None = None

    dpi: int | None = None


class ThemeResponse(ThemeBase):

    id: int

    class Config:
        from_attributes = True