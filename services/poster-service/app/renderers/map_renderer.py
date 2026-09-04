from matplotlib.patches import Polygon


def draw_map(
    ax,
    map_data,
    theme,
):

    # =========================
    # PARKS
    # =========================

    for park in map_data.get("parks", []):

        coordinates = park.get(
            "coordinates",
            [],
        )

        if len(coordinates) < 3:
            continue

        polygon = Polygon(
            coordinates,
            closed=True,
            facecolor=theme["parks"],
            edgecolor="none",
        )

        ax.add_patch(polygon)

    # =========================
    # WATER
    # =========================

    for water in map_data.get("water", []):

        coordinates = water.get(
            "coordinates",
            [],
        )

        if len(coordinates) < 3:
            continue

        polygon = Polygon(
            coordinates,
            closed=True,
            facecolor=theme["water"],
            edgecolor="none",
        )

        ax.add_patch(polygon)

    # =========================
    # ROADS
    # =========================

    for road in map_data.get("roads", []):

        coordinates = road.get(
            "coordinates",
            [],
        )

        if len(coordinates) < 2:
            continue

        road_type = road.get(
            "type",
            "default",
        )

        color = theme["roads"].get(
            road_type,
            theme["roads"]["default"],
        )

        width = theme["road_widths"].get(
            road_type,
            theme["road_widths"]["default"],
        )

        xs = [
            point[0]
            for point in coordinates
        ]

        ys = [
            point[1]
            for point in coordinates
        ]

        ax.plot(
            xs,
            ys,
            color=color,
            linewidth=width,
            solid_capstyle="round",
            solid_joinstyle="round",
        )