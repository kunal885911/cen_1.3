# Generating CAD File using cadquery
def generate_shaft_step_file(params_dict: dict, step_path: str):
    diameter = params_dict["diameter"]
    length = params_dict["length"]
    keyway_length = 0.8 * length - 0.5
    KEYWAY_TABLE = [
    (22, 6, 2.8),
    (30, 8, 3.3),
    (38, 10, 3.3),
    (44, 12, 3.3),
    (50, 14, 3.8),
    (65, 18, 4.4),
    (85, 22, 5.4),
    (105, 28, 6.9),
    (130, 32, 7.4),
]
    def get_keyway(diameter):
        for limit, width, height in KEYWAY_TABLE:
            if diameter <= limit:
                return width, height
        raise ValueError("No keyway defined")
    keyway_width, keyway_height = get_keyway(diameter)
    # keyway_width = diameter * 0.3
    # keyway_height = diameter * 0.1
    radius = 0
    if diameter <= 12:
        radius = 0.16
    elif diameter < 22:
        radius = 0.25
    elif diameter < 38:
        radius = 0.40
    elif diameter < 58:
        radius = 0.60
    elif diameter < 110:
        radius = 1.00
    elif diameter < 170:
        radius = 1.60
    elif diameter <= 500:
        radius = 2.50
    try:
        import cadquery as cq  # type: ignore
        shaft = cq.Workplane("XY").circle(diameter / 2).extrude(length)
        shaft = (
            shaft.faces(">Z")
            .workplane()
            .center(0, diameter / 2 - keyway_height / 2)
            .slot2D(keyway_width, keyway_height)
            .cutBlind(-keyway_length)
            )
        safe_radius = min(radius, keyway_height / 2 - 0.2)
        shaft = shaft.edges("|Z").fillet(safe_radius)
        cq.exporters.export(shaft, str(step_path), "STEP")
    except Exception as exc:
        print("ERROR IN PROCESS:", exc)
        raise exc