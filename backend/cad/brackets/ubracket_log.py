from schemas.ubracket_schema import UbracketParams
def ubracket_logs(params: UbracketParams):
    return [
        "Process started",
        f"Model type: Ubracket",
        f"Length: {params.length} mm",
        f"Height: {params.height} mm",
        f"Width: {params.width} mm",
        "STEP export complete",
        "Bundle generation complete",
    ]