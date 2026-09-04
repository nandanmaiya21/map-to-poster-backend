from app.database import Base, engine
from app.models.map import Map


def init_db():
    Base.metadata.create_all(
        bind=engine
    )