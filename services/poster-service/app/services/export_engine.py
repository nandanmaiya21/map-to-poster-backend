import os


EXPORT_DIR = "/app/app/exports"


SUPPORTED_FORMATS = {
    "png",
    "svg",
    "pdf",
}


def export_poster(
    figure,
    map_id: str,
    theme_slug: str,
    export_format: str,
    dpi: int,
    background_color: str,
):
    """
    Export poster figure in requested format.
    """

    # =====================================
    # VALIDATE FORMAT
    # =====================================

    export_format = export_format.lower()

    if export_format not in SUPPORTED_FORMATS:

        raise ValueError(
            f"Unsupported export format: {export_format}"
        )

    # =====================================
    # CREATE EXPORT DIRECTORY
    # =====================================

    os.makedirs(
        EXPORT_DIR,
        exist_ok=True,
    )

    # =====================================
    # BUILD FILENAME
    # =====================================

    filename = (
        f"{map_id}_{theme_slug}.{export_format}"
    )

    output_path = os.path.join(
        EXPORT_DIR,
        filename,
    )

    # =====================================
    # PNG EXPORT
    # =====================================

    if export_format == "png":

        figure.savefig(
            output_path,
            format="png",
            dpi=dpi,
            facecolor=background_color,
            pad_inches=0,
        )

    # =====================================
    # SVG EXPORT
    # =====================================

    elif export_format == "svg":

        figure.savefig(
            output_path,
            format="svg",
            facecolor=background_color,
            pad_inches=0,
        )

    # =====================================
    # PDF EXPORT
    # =====================================

    elif export_format == "pdf":

        figure.savefig(
            output_path,
            format="pdf",
            dpi=dpi,
            facecolor=background_color,
            pad_inches=0,
        )

    print(
        f"✓ Exported poster: {output_path}",
        flush=True,
    )

    return output_path