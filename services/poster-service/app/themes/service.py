from sqlalchemy.orm import Session

from app.models.theme import ThemeModel


def get_theme_by_slug(
    db: Session,
    slug: str,
):
    return (
        db.query(ThemeModel)
        .filter(
            ThemeModel.slug == slug.lower()
        )
        .first()
    )


def get_all_themes(
    db: Session,
):
    return (
        db.query(ThemeModel)
        .order_by(
            ThemeModel.created_at.desc()
        )
        .all()
    )


def create_theme(
    db: Session,
    theme_data,
):

    theme = ThemeModel(
        **theme_data.model_dump()
    )

    theme.slug = theme.slug.lower()

    db.add(theme)
    db.commit()
    db.refresh(theme)

    return theme


def update_theme(
    db: Session,
    theme: ThemeModel,
    theme_data,
):

    update_data = theme_data.model_dump(
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


def delete_theme(
    db: Session,
    theme: ThemeModel,
):

    db.delete(theme)
    db.commit()