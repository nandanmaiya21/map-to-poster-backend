from fastapi import (
    FastAPI,
    HTTPException,
    Depends,
)

from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from app.database import (
    engine,
    SessionLocal,
)

from app.models.base import Base

# Import model so SQLAlchemy registers it
from app.models.theme import ThemeModel

from app.clients.map_client import get_map_data
from app.renderers.poster_renderer import render_poster

from app.schemas.poster import PosterRenderRequest

from app.routes.themes import (
    router as themes_router,
)
from app.services.theme_adapter import (
    theme_model_to_render_theme,
)
from app.services.render_settings import (
    build_render_settings,
)
import traceback


# =====================================
# CREATE DATABASE TABLES
# =====================================

Base.metadata.create_all(
    bind=engine
)


# =====================================
# FASTAPI
# =====================================

app = FastAPI(
    title="Poster Service",
)




# =====================================
# STATIC EXPORTS
# =====================================

app.mount(
    "/exports",
    StaticFiles(directory="/app/app/exports"),
    name="exports",
)


# =====================================
# THEME ROUTES
# =====================================

app.include_router(
    themes_router
)


# =====================================
# DATABASE DEPENDENCY
# =====================================

def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# =====================================
# HEALTH
# =====================================

@app.get("/health")
def health():

    return {
        "status": "ok",
        "service": "poster-service",
    }


# =====================================
# RENDER POSTER
# =====================================

@app.post("/render/{map_id}")
async def render_map_poster(
    map_id: str,
    request: PosterRenderRequest,
    db: Session = Depends(get_db),
):

    try:

        # =====================================
        # GET MAP DATA
        # =====================================

        map_response = await get_map_data(
            map_id
        )

        # =====================================
        # CHECK MAP STATUS
        # =====================================

        if map_response["status"] != "completed":

            return {
                "map_id": map_id,
                "status": map_response["status"],
                "message": "Map data is not ready yet",
            }

        # =====================================
        # GET GEOMETRY
        # =====================================

        map_data = map_response.get("data")

        if not map_data:

            raise HTTPException(
                status_code=400,
                detail="Map has no geometry data",
            )

        # =====================================
        # LOAD THEME FROM DATABASE
        # =====================================

        theme = (
            db.query(ThemeModel)
            .filter(
                ThemeModel.slug
                == request.theme.lower()
            )
            .first()
        )

        if not theme:

            raise HTTPException(
                status_code=404,
                detail=(
                    f"Theme '{request.theme}' "
                    "not found"
                ),
            )

        render_theme = theme_model_to_render_theme(theme)

        render_settings = build_render_settings(
        theme=theme,
        request=request,
        )

        # =====================================
        # RENDER POSTER
        # =====================================



        output_path = render_poster(
            map_id=map_id,
            map_data=map_data,
            theme=render_theme,
            settings=render_settings,
            title=request.title,
            subtitle=request.subtitle,
            coordinates=request.coordinates,
           
        )

        filename = output_path.split("/")[-1]

        # =====================================
        # RESPONSE
        # =====================================

        return {
            "status": "completed",
            "map_id": map_id,
            "theme": theme.slug,
            "title": request.title,
            "subtitle": request.subtitle,
            "coordinates": request.coordinates,
            "file": filename,
            "url": f"/exports/{filename}",
        }

    except HTTPException:
        raise

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

    except Exception as error:

        print(
            "\n========== POSTER RENDER ERROR ==========",
            flush=True,
        )

        traceback.print_exc()

        print(
            "=========================================\n",
            flush=True,
        )

        raise HTTPException(
        status_code=500,
        detail=str(error),
        )
