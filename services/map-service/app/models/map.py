from sqlalchemy import Column, String, Float, Text
from sqlalchemy.dialects.postgresql import JSONB
from geoalchemy2 import Geometry

from app.database import Base


class Map(Base):
    __tablename__ = "maps"

    id = Column(
        String,
        primary_key=True,
        index=True,
    )

    status = Column(
        String,
        nullable=False,
        default="processing",
    )

    latitude = Column(
        Float,
        nullable=False,
    )

    longitude = Column(
        Float,
        nullable=False,
    )

    radius = Column(
        Float,
        nullable=False,
    )

    # Coverage area this map was generated for - either the real
    # city administrative boundary (Polygon or MultiPolygon, when
    # place-based generation resolved a city) or, as a fallback,
    # the rectangular bbox osmnx fetches via dist_type="bbox".
    # Used to answer "is this GPS point already covered by an
    # existing map?" via PostGIS ST_Contains, instead of comparing
    # exact coordinates. Generic "GEOMETRY" type since a city
    # boundary's subtype isn't known upfront (islands/exclaves
    # make some cities MultiPolygon).
    boundary = Column(
        Geometry(geometry_type="GEOMETRY", srid=4326),
        nullable=True,
    )

    data = Column(
        JSONB,
        nullable=True,
    )

    error = Column(
        Text,
        nullable=True,
    )