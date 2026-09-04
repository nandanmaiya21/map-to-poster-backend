def calculate_map_bounds(
    roads,
    water,
    parks,
    poster_width,
    poster_height,
    padding=0.08,
    text_space=0.22,
):
    """
    Calculate poster-aware map bounds.

    - Fits all geometry
    - Adds padding
    - Matches poster aspect ratio
    - Reserves visual space for bottom typography
    """

    xs = []
    ys = []

    # =====================================
    # COLLECT ROAD COORDINATES
    # =====================================

    for road in roads:

        coordinates = road.get(
            "coordinates",
            [],
        )

        for point in coordinates:

            if len(point) >= 2:

                xs.append(point[0])
                ys.append(point[1])

    # =====================================
    # COLLECT WATER COORDINATES
    # =====================================

    for feature in water:

        coordinates = feature.get(
            "coordinates",
            [],
        )

        for point in coordinates:

            if len(point) >= 2:

                xs.append(point[0])
                ys.append(point[1])

    # =====================================
    # COLLECT PARK COORDINATES
    # =====================================

    for feature in parks:

        coordinates = feature.get(
            "coordinates",
            [],
        )

        for point in coordinates:

            if len(point) >= 2:

                xs.append(point[0])
                ys.append(point[1])

    # =====================================
    # VALIDATE
    # =====================================

    if not xs or not ys:

        raise ValueError(
            "Unable to calculate map bounds"
        )

    xmin = min(xs)
    xmax = max(xs)

    ymin = min(ys)
    ymax = max(ys)

    map_width = xmax - xmin
    map_height = ymax - ymin

    # Prevent zero-size bounds

    if map_width == 0:
        map_width = 1

    if map_height == 0:
        map_height = 1

    # =====================================
    # ADD PADDING
    # =====================================

    padding_x = map_width * padding
    padding_y = map_height * padding

    xmin -= padding_x
    xmax += padding_x

    ymin -= padding_y
    ymax += padding_y

    map_width = xmax - xmin
    map_height = ymax - ymin

    # =====================================
    # POSTER ASPECT RATIO
    # =====================================

    poster_ratio = (
        poster_width
        / poster_height
    )

    map_ratio = (
        map_width
        / map_height
    )

    # =====================================
    # EXPAND MAP TO MATCH POSTER RATIO
    # =====================================

    center_x = (
        xmin + xmax
    ) / 2

    center_y = (
        ymin + ymax
    ) / 2

    if map_ratio > poster_ratio:

        # Map is too wide
        # Expand height

        target_height = (
            map_width
            / poster_ratio
        )

        half_height = (
            target_height / 2
        )

        ymin = (
            center_y
            - half_height
        )

        ymax = (
            center_y
            + half_height
        )

    else:

        # Map is too tall
        # Expand width

        target_width = (
            map_height
            * poster_ratio
        )

        half_width = (
            target_width / 2
        )

        xmin = (
            center_x
            - half_width
        )

        xmax = (
            center_x
            + half_width
        )

    # =====================================
    # SHIFT MAP UP
    #
    # Reserve space for typography
    # =====================================

    final_height = ymax - ymin

    shift = (
        final_height
        * text_space
    )

    ymin -= shift
    ymax -= shift

    return (
        xmin,
        xmax,
        ymin,
        ymax,
    )