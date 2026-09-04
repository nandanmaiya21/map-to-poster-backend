from app.schemas.render_settings import (
    RenderSettings,
)


def build_render_settings(
    theme,
    request,
):

    return RenderSettings(

        # User overrides theme defaults

        width=(
            request.width
            if request.width
            else theme.width
        ),

        height=(
            request.height
            if request.height
            else theme.height
        ),

        dpi=(
            request.dpi
            if request.dpi
            else theme.dpi
        ),


        # Map

        map_padding=request.map_padding,

        map_coverage=request.map_coverage,


        # Visibility

        show_title=request.show_title,

        show_subtitle=request.show_subtitle,

        show_coordinates=request.show_coordinates,

        show_attribution=request.show_attribution,


        # Layout

        layout=request.layout,
    )