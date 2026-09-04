from app.schemas.render_theme import RenderTheme


def theme_model_to_render_theme(theme) -> RenderTheme:

    return RenderTheme(
        name=theme.name,

        background=theme.background,

        water_color=theme.water_color,
        park_color=theme.park_color,

        road_colors=theme.road_colors,
        road_widths=theme.road_widths,

        text_primary=theme.text_primary,
        text_secondary=theme.text_secondary,

        font_family=theme.font_family,

        width=theme.width,
        height=theme.height,
        dpi=theme.dpi,
    )