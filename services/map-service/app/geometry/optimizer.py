IMPORTANT_ROADS = {
    "motorway",
    "trunk",
    "primary",
    "secondary",
    "tertiary",
    "residential",
    "unclassified",
    "service",
    "living_street",
}


def optimize_roads(roads):

    optimized = []

    seen = set()

    for road in roads:

        road_type = road.get(
            "type",
            "unclassified"
        )

        # Remove unwanted tiny paths
        if road_type not in IMPORTANT_ROADS:
            continue

        coordinates = road.get(
            "coordinates",
            []
        )

        if len(coordinates) < 2:
            continue

        # Remove exact duplicates
        road_key = str(coordinates)

        if road_key in seen:
            continue

        seen.add(road_key)

        optimized.append({
            "type": road_type,
            "coordinates": coordinates,
        })

    return optimized