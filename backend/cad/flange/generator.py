from math import ceil, sqrt, pi, cos, sin

BOLT_TABLE = [
    (5.0, "M5", 5.5),
    (6.0, "M6", 6.6),
    (8.0, "M8", 9.0),
    (10.0, "M10", 11.0),
    (12.0, "M12", 13.5),
    (14.0, "M14", 15.5),
    (16.0, "M16", 17.5),
    (20.0, "M20", 22.0),
    (24.0, "M24", 26.0),
    (30.0, "M30", 33.0),
    (36.0, "M36", 39.0),
]

def get_bolt_size(d1: float):
    for limit, name, hole_diameter in BOLT_TABLE:
        if d1 <= limit:
            return name, hole_diameter
    raise ValueError("No suitable bolt size found")

def generate_flange_step_file(params_dict: dict, step_path: str):
    inner_diameter = params_dict["inner_diameter"]
    thickness = 0.25 * inner_diameter
    bolt_circle = 2.5 * inner_diameter
    outer_diameter = bolt_circle + (1.2 * inner_diameter)
    hub_diameter = 1.8 * inner_diameter
    hub_height = 1.2 * thickness

    if inner_diameter <= 50:
        bolt_count = 4
    elif inner_diameter <= 100:
        bolt_count = 6
    elif inner_diameter <= 200:
        bolt_count = 8
    else:
        bolt_count = 12

    d1 = (0.5 * inner_diameter) / sqrt(bolt_count)
    bolt_name, bolt_hole_diameter = get_bolt_size(d1)
    print(f"total bolt count is {bolt_count}")
    
    points = []
    for i in range(bolt_count):
        angle = 2 * pi * i / bolt_count
        x = (bolt_circle / 2) * cos(angle)
        y = (bolt_circle / 2) * sin(angle)
        points.append((x, y))
        
    try:
        import cadquery as cq # type: ignore
        flange = cq.Workplane("XY").circle(outer_diameter / 2).extrude(thickness)
        hub = cq.Workplane("XY").circle(hub_diameter / 2).extrude(hub_height)
        flange = flange.union(hub)
        flange = flange.faces(">Z").workplane().hole(inner_diameter)
        flange = flange.faces(">Z").workplane().pushPoints(points).hole(bolt_hole_diameter)
        try:
            flange = flange.edges("|Z").fillet(min(1.5, thickness / 4))
        except:
            pass
        cq.exporters.export(flange, str(step_path), "STEP")
    except Exception as exc:
        print("ERROR IN PROCESS:", exc)
        raise exc