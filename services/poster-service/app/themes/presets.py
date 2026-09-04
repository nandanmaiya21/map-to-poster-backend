from app.themes.schema import Theme


THEMES = {

    "midnight": Theme(
        name="Midnight",

        background="#0B0D12",

        water_color="#132238",
        park_color="#172B20",

        road_colors={
            "motorway": "#F5F5F5",
            "trunk": "#E0E0E0",
            "primary": "#CFCFCF",
            "secondary": "#8A8A8A",
            "tertiary": "#5E5E5E",
            "residential": "#383838",
            "unclassified": "#303030",
            "default": "#252525",
        },

        road_widths={
            "motorway": 2.2,
            "trunk": 1.8,
            "primary": 1.5,
            "secondary": 1.0,
            "tertiary": 0.8,
            "residential": 0.45,
            "unclassified": 0.4,
            "default": 0.3,
        },

        text_primary="#FFFFFF",
        text_secondary="#8A8A8A",

        font_family="DejaVu Sans",
    ),


    "blueprint": Theme(
        name="Blueprint",

        background="#071E3D",

        water_color="#0A2A52",
        park_color="#123B3A",

        road_colors={
            "motorway": "#FFFFFF",
            "trunk": "#D9EFFF",
            "primary": "#B9D9F5",
            "secondary": "#6FA3D2",
            "tertiary": "#477BA8",
            "residential": "#315D82",
            "unclassified": "#294D6B",
            "default": "#203F5A",
        },

        road_widths={
            "motorway": 2.0,
            "trunk": 1.6,
            "primary": 1.3,
            "secondary": 0.9,
            "tertiary": 0.7,
            "residential": 0.4,
            "unclassified": 0.35,
            "default": 0.25,
        },

        text_primary="#FFFFFF",
        text_secondary="#82B1D6",

        font_family="DejaVu Sans",
    ),


    "minimal": Theme(
        name="Minimal",

        background="#F4F1EA",

        water_color="#D6E5EA",
        park_color="#DCE8D5",

        road_colors={
            "motorway": "#111111",
            "trunk": "#222222",
            "primary": "#333333",
            "secondary": "#555555",
            "tertiary": "#777777",
            "residential": "#999999",
            "unclassified": "#AAAAAA",
            "default": "#CCCCCC",
        },

        road_widths={
            "motorway": 2.2,
            "trunk": 1.8,
            "primary": 1.4,
            "secondary": 1.0,
            "tertiary": 0.7,
            "residential": 0.4,
            "unclassified": 0.35,
            "default": 0.25,
        },

        text_primary="#111111",
        text_secondary="#666666",

        font_family="DejaVu Sans",
    ),
}