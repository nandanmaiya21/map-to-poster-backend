from pyproj import Transformer


transformer = Transformer.from_crs(
    "EPSG:4326",
    "EPSG:3857",
    always_xy=True,
)


def project_coordinate(lon: float, lat: float):

    if lon is None or lat is None:
        raise ValueError("Invalid coordinate")

    x, y = transformer.transform(
        float(lon),
        float(lat),
    )

    return [
        round(x, 3),
        round(y, 3),
    ]


def project_coordinates(coordinates):

    if not coordinates:
        return []

    return [
        project_coordinate(lon, lat)
        for lon, lat in coordinates
    ]