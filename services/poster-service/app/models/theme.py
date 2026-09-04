from sqlalchemy import (
    Column,
    Integer,
    String,
    JSON,
)

from app.models.base import Base


class ThemeModel(Base):

    __tablename__ = "themes"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    slug = Column(
        String,
        unique=True,
        nullable=False,
        index=True,
    )

    name = Column(
        String,
        nullable=False,
    )

    background = Column(
        String,
        nullable=False,
    )

    water_color = Column(
        String,
        nullable=False,
    )

    park_color = Column(
        String,
        nullable=False,
    )

    road_colors = Column(
        JSON,
        nullable=False,
    )

    road_widths = Column(
        JSON,
        nullable=False,
    )

    text_primary = Column(
        String,
        nullable=False,
    )

    text_secondary = Column(
        String,
        nullable=False,
    )

    font_family = Column(
        String,
        nullable=False,
        default="DejaVu Sans",
    )

    width = Column(
        Integer,
        nullable=False,
        default=2000,
    )

    height = Column(
        Integer,
        nullable=False,
        default=3000,
    )

    dpi = Column(
        Integer,
        nullable=False,
        default=300,
    )