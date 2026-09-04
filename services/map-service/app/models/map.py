from sqlalchemy import Column, String, Float, Text
from sqlalchemy.dialects.postgresql import JSONB

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

    data = Column(
        JSONB,
        nullable=True,
    )

    error = Column(
        Text,
        nullable=True,
    )