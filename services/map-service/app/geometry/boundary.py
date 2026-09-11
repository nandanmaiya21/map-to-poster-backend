from geoalchemy2.elements import WKTElement
from geoalchemy2.shape import from_shape

from app.osm.bounds import calculate_bounds


def build_map_boundary(latitude, longitude, radius):
    """
    Build the rectangular coverage boundary for a map request.

    Matches the bbox osmnx actually fetches (dist_type="bbox" in
    fetch_street_network), so a point falling inside this polygon
    is guaranteed to already be covered by this map's data.
    """

    bounds = calculate_bounds(latitude, longitude, radius)

    south = bounds["south"]
    north = bounds["north"]
    west = bounds["west"]
    east = bounds["east"]

    wkt = (
        f"POLYGON(("
        f"{west} {south}, {east} {south}, "
        f"{east} {north}, {west} {north}, "
        f"{west} {south}))"
    )

    return WKTElement(wkt, srid=4326)


def build_city_boundary(boundary_gdf):
    """
    Convert a place's real administrative boundary, as returned by
    osm.client.fetch_city_boundary (ox.geocode_to_gdf), into a
    PostGIS-storable geometry. This is the actual city shape, not
    an approximation - may be a Polygon or MultiPolygon.
    """

    geometry = boundary_gdf.geometry.iloc[0]

    return from_shape(geometry, srid=4326)
