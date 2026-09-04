from shapely.geometry import (
    LineString,
    MultiLineString,
)


SIMPLIFY_TOLERANCE = 0.00001


def line_to_coordinates(geometry):

    geometry = geometry.simplify(
        SIMPLIFY_TOLERANCE,
        preserve_topology=True,
    )

    return [
        [
            round(float(lon), 7),
            round(float(lat), 7),
        ]
        for lon, lat in geometry.coords
    ]


def extract_roads(graph):

    roads = []

    for u, v, key, data in graph.edges(
        keys=True,
        data=True,
    ):

        geometry = data.get("geometry")

        # Some OSM edges don't have geometry
        if geometry is None:

            start = graph.nodes[u]
            end = graph.nodes[v]

            geometry = LineString([
                (start["x"], start["y"]),
                (end["x"], end["y"]),
            ])

        highway = data.get(
            "highway",
            "unclassified",
        )

        if isinstance(highway, list):
            highway = highway[0]

        # =============================
        # SINGLE LINE
        # =============================

        if isinstance(geometry, LineString):

            coordinates = line_to_coordinates(
                geometry
            )

            if len(coordinates) >= 2:

                roads.append({
                    "type": str(highway),
                    "coordinates": coordinates,
                })

        # =============================
        # MULTIPLE LINES
        # =============================

        elif isinstance(geometry, MultiLineString):

            for line in geometry.geoms:

                coordinates = line_to_coordinates(
                    line
                )

                if len(coordinates) >= 2:

                    roads.append({
                        "type": str(highway),
                        "coordinates": coordinates,
                    })

    return roads