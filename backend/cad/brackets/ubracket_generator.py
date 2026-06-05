# Generating CAD File using cadquery 
def generate_ubracket_step_file(params_dict: dict, step_path: str):
    try:
        import cadquery as cq  # type: ignore
        length = params_dict["length"]
        height = params_dict["height"]
        width = params_dict["width"]
        thickness = 0.1 * width
        bend_fillets = min(0.5 * thickness, thickness * 0.4)
        base = cq.Workplane("XY").rect(length, width).extrude(thickness)
        left_wall = cq.Workplane("XY").rect(length, thickness).extrude(height).translate((0, -width/2 + thickness/2, thickness))
        right_wall = cq.Workplane("XY").rect(length, thickness).extrude(height).translate((0, width/2 - thickness/2, thickness))
        bracket = base.union(left_wall).union(right_wall)
        bracket = bracket.edges("|Z").fillet(bend_fillets)
        cq.exporters.export(bracket, str(step_path), "STEP")
    except Exception as exc:
        print("ERROR IN PROCESS:", exc)
        raise exc