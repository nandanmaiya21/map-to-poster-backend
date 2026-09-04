from app.themes.presets import THEMES


def get_theme(theme_name: str):
    """
    Get a theme by its key.

    Example:
        get_theme("midnight")
    """

    if not theme_name:
        return None

    return THEMES.get(
        theme_name.lower()
    )


def get_all_themes():
    """
    Return all available themes.
    """

    return THEMES


def get_theme_names():
    """
    Return available theme keys.
    """

    return list(THEMES.keys())