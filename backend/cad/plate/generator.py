# Generating CAD File using cadquery
def generate_plate_step_file(params_dict: dict, step_path: str):
    length = params_dict["length"]
    width = params_dict["width"]
    thicknees = max(6.0, 0.05 * width)
    corner_fillets = 0.5 * thicknees
    try:
        import cadquery as cq  # type: ignore
        plate = cq.Workplane("XY").box(length, width, thicknees)
        plate = plate.edges("|Z").fillet(corner_fillets)
        cq.exporters.export(plate, str(step_path), "STEP")
    except Exception as exc:
        print("ERROR IN PROCESS:", exc)
        raise exc