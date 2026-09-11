from sqlalchemy import text

from app.database import Base, engine
from app.models.map import Map


def init_db():

    with engine.connect() as conn:
        conn.execute(
            text("CREATE EXTENSION IF NOT EXISTS postgis")
        )
        conn.commit()

    Base.metadata.create_all(
        bind=engine
    )

    # create_all() only creates missing tables - it won't add a new
    # column, or widen an existing column's type, on a "maps" table
    # that already exists, so do both explicitly here.
    with engine.connect() as conn:
        conn.execute(
            text(
                "ALTER TABLE maps "
                "ADD COLUMN IF NOT EXISTS boundary "
                "geometry(Geometry, 4326)"
            )
        )
        conn.execute(
            text(
                "ALTER TABLE maps "
                "ALTER COLUMN boundary TYPE geometry(Geometry, 4326) "
                "USING boundary::geometry(Geometry, 4326)"
            )
        )
        conn.execute(
            text(
                "CREATE INDEX IF NOT EXISTS idx_maps_boundary "
                "ON maps USING GIST (boundary)"
            )
        )
        conn.commit()