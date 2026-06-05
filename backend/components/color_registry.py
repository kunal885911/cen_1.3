COMPONENT_COLORS = {
    "shaft":          {"r": 0.65, "g": 0.65, "b": 0.70, "name": "Steel Gray"},
    "flange":         {"r": 0.80, "g": 0.50, "b": 0.20, "name": "Brass Orange"},
    "plate":          {"r": 0.20, "g": 0.55, "b": 0.80, "name": "Steel Blue"},
    "cylinder":       {"r": 0.30, "g": 0.70, "b": 0.40, "name": "Anodized Green"},
    "pipe":           {"r": 0.70, "g": 0.20, "b": 0.20, "name": "Oxide Red"},
    "lbracket":       {"r": 0.85, "g": 0.75, "b": 0.10, "name": "Zinc Yellow"},
    "ubracket":       {"r": 0.50, "g": 0.20, "b": 0.70, "name": "Anodized Purple"},
    "housing":        {"r": 0.20, "g": 0.40, "b": 0.30, "name": "Gunmetal Green"},
}

def get_color(component_type: str) -> dict:
    """Return color dict for a component type. Falls back to gray."""
    return COMPONENT_COLORS.get(component_type,
           {"r": 0.5, "g": 0.5, "b": 0.5, "name": "Default Gray"})
