from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.theme import ThemeModel

from app.schemas.theme import (
    ThemeCreate,
    ThemeUpdate,
    ThemeResponse,
)
from app.security.admin import require_admin

router = APIRouter(
    prefix="/themes",
    tags=["Themes"],
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
# CREATE THEME
# =====================================

@router.post(
    "",
    response_model=ThemeResponse,
    status_code=201,
)
def create_theme(
    theme: ThemeCreate,
    db: Session = Depends(get_db),
    _: bool = Depends(require_admin),
):

    existing_theme = (
        db.query(ThemeModel)
        .filter(
            ThemeModel.slug == theme.slug.lower()
        )
        .first()
    )

    if existing_theme:

        raise HTTPException(
            status_code=409,
            detail="Theme slug already exists",
        )

    theme_data = theme.model_dump()

    # Normalize slug
    theme_data["slug"] = (
        theme_data["slug"]
        .lower()
        .strip()
    )

    new_theme = ThemeModel(
        **theme_data
    )

    db.add(new_theme)
    db.commit()
    db.refresh(new_theme)

    return new_theme


# =====================================
# GET ALL THEMES
# =====================================

@router.get(
    "",
    response_model=list[ThemeResponse],
)
def get_themes(
    db: Session = Depends(get_db),
):

    themes = (
        db.query(ThemeModel)
        .order_by(ThemeModel.id.asc())
        .all()
    )

    return themes


# =====================================
# GET SINGLE THEME
# =====================================

@router.get(
    "/{slug}",
    response_model=ThemeResponse,
)
def get_theme(
    slug: str,
    db: Session = Depends(get_db),
):

    theme = (
        db.query(ThemeModel)
        .filter(
            ThemeModel.slug == slug.lower()
        )
        .first()
    )

    if not theme:

        raise HTTPException(
            status_code=404,
            detail="Theme not found",
        )

    return theme


# =====================================
# UPDATE THEME
# =====================================

@router.put(
    "/{slug}",
    response_model=ThemeResponse,
    
)
def update_theme(
    slug: str,
    theme_update: ThemeUpdate,
    db: Session = Depends(get_db),
    _: bool = Depends(require_admin),
):

    theme = (
        db.query(ThemeModel)
        .filter(
            ThemeModel.slug == slug.lower()
        )
        .first()
    )

    if not theme:

        raise HTTPException(
            status_code=404,
            detail="Theme not found",
        )

    update_data = theme_update.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():

        setattr(
            theme,
            field,
            value,
        )

    db.commit()
    db.refresh(theme)

    return theme


# =====================================
# DELETE THEME
# =====================================

@router.delete(
    "/{slug}",
)
def delete_theme(
    slug: str,
    db: Session = Depends(get_db),
    _: bool = Depends(require_admin),
):

    theme = (
        db.query(ThemeModel)
        .filter(
            ThemeModel.slug == slug.lower()
        )
        .first()
    )

    if not theme:

        raise HTTPException(
            status_code=404,
            detail="Theme not found",
        )

    db.delete(theme)
    db.commit()

    return {
        "status": "deleted",
        "slug": slug.lower(),
    }