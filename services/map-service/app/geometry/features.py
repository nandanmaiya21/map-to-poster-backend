from shapely.geometry import (
    Polygon,
    MultiPolygon,
    LineString,
    MultiLineString,
)


SIMPLIFY_TOLERANCE = 0.00001


def polygon_to_coordinates(polygon):

    geometry = polygon.simplify(
        SIMPLIFY_TOLERANCE,
        preserve_topology=True
    )

    return [
        [
            round(float(lon), 7),
            round(float(lat), 7)
        ]
        for lon, lat in geometry.exterior.coords
    ]


def extract_polygons(geodata):

    features = []

    if geodata is None or geodata.empty:
        return features

    for _, row in geodata.iterrows():

        geometry = row.geometry

        if geometry is None:
            continue

        # ========================
        # SINGLE POLYGON
        # ========================

        if isinstance(geometry, Polygon):

            coordinates = polygon_to_coordinates(
                geometry
            )

            if len(coordinates) >= 3:

                features.append({
                    "coordinates": coordinates
                })

        # ========================
        # MULTI POLYGON
        # ========================

        elif isinstance(geometry, MultiPolygon):

            for polygon in geometry.geoms:

                coordinates = polygon_to_coordinates(
                    polygon
                )

                if len(coordinates) >= 3:

                    features.append({
                        "coordinates": coordinates
                    })

    return features