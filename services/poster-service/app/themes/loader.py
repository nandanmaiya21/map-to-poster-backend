from app.themes.presets import THEMES


def get_theme(theme_name: str):

    theme_name = theme_name.lower()

    theme = THEMES.get(theme_name)

    if theme is None:

        raise ValueError(
            f"Theme '{theme_name}' not found"
        )

    return theme


def list_themes():

    return [
        {
            "id": key,
            "name": theme.name,
        }
        for key, theme in THEMES.items()
    ]