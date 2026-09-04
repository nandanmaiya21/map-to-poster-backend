from app.schemas.render_settings import RenderSettings


def build_render_settings(
    theme,
    request,
):

    return RenderSettings(

        # Poster
        width=request.width or theme.width,
        height=request.height or theme.height,
        dpi=request.dpi or theme.dpi,


        # Map Camera
        map_padding=request.map_padding,
        map_coverage=request.map_coverage,
        map_offset_x=request.map_offset_x,
        map_offset_y=request.map_offset_y,


        # Typography
        title_size=request.title_size,
        subtitle_size=request.subtitle_size,
        coordinates_size=request.coordinates_size,
        font_weight=request.font_weight,


        # Gradients
        show_top_gradient=request.show_top_gradient,
        show_bottom_gradient=request.show_bottom_gradient,
        gradient_height=request.gradient_height,
        gradient_strength=request.gradient_strength,


        # Divider
        show_divider=request.show_divider,
        divider_width=request.divider_width,


        # Display
        show_title=request.show_title,
        show_subtitle=request.show_subtitle,
        show_coordinates=request.show_coordinates,
        show_attribution=request.show_attribution,


        # Layout
        layout=request.layout,
        #Export
        export_format=request.export_format,
    )