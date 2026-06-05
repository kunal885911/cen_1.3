# Generating CAD File using cadquery 
def generate_lbracket_step_file(params_dict: dict, step_path: str):
    try:
        import cadquery as cq  # type: ignore
        length_1 = params_dict["length_1"]
        length_2 = params_dict["length_2"]
        width = params_dict["width"]
        thickness = 0.1 * width
        bend_fillets = min(0.5 * thickness, thickness * 0.4, min(length_1, length_2))
        bracket = (
            cq.Workplane("XY")
            .polyline([(0, 0), (length_1, 0), (length_1, thickness), (thickness, thickness), (thickness, length_2), (0, length_2)])
            .close()
            .extrude(thickness)
            )
        bracket = bracket.edges("|Z").fillet(bend_fillets)
        cq.exporters.export(bracket, str(step_path), "STEP")
    except Exception as exc:
        print("ERROR IN PROCESS:", exc)
        raise exc