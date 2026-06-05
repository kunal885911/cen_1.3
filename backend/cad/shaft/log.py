from schemas.shaft_schema import ShaftParams
def shaft_logs(params: ShaftParams):
    return [
        "Process started",
        f"Model type: shaft",
        f"Diameter: {params.diameter} mm",
        f"Length: {params.length} mm",
        "STEP export complete",
        "Bundle generation complete",
    ]