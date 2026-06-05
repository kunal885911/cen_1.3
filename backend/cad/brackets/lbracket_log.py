from schemas.Lbracket_schema import LbracketParams
def lbracket_logs(params: LbracketParams):
    return [
        "Process started",
        f"Model type: Lbracket",
        f"Length1: {params.length_1} mm",
        f"Length2: {params.length_2} mm",
        f"Width: {params.width} mm",
        "STEP export complete",
        "Bundle generation complete",
    ]