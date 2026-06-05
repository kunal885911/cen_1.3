from schemas.plate_schema import PlateParams
def plate_logs(params: PlateParams):
    return [
        "Process started",
        f"Model type: plate",
        f"Length: {params.length} mm",
        f"Width: {params.width} mm",
        "STEP export complete",
        "Bundle generation complete",
    ]