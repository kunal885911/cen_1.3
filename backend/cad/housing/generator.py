
# Generating CAD File using cadquery 
def generate_housing_step_file(params_dict: dict, step_path: str):
    try:
        import cadquery as cq  # type: ignore
        length = params_dict["length"]
        height = params_dict["height"]
        width = params_dict["width"]
        wall_thickness = max(6.0, 0.1 * min(width, height) + 7.5)
        fillets = 0.5 * wall_thickness
        outer = cq.Workplane("XY").rect(length, width).extrude(height)
        inner = (
            cq.Workplane("XY")
            .rect(length - 2 * wall_thickness, width - 2 * wall_thickness)
            .extrude(height - wall_thickness)
            .translate((0, 0, wall_thickness))
            )
        housing = outer.cut(inner)
        housing = housing.edges("|Z").fillet(fillets)
        cq.exporters.export(housing, str(step_path), "STEP")
    except Exception as exc:
        print("ERROR IN PROCESS:", exc)
        raise exc