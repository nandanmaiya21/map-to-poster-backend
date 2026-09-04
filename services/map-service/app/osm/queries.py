def build_map_query(
    south: float,
    west: float,
    north: float,
    east: float
) -> str:

    return f"""
    [out:json][timeout:60];

    (
      way["highway"]
        ({south},{west},{north},{east});
    );

    out body;
    >;
    out skel qt;
    """