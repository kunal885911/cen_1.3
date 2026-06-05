from schemas.housing_schema import HousingParams
def housing_logs(params: HousingParams):
    return [
        "Process started",
        "Model type: housing",
        f"Length: {params.length} mm",
        f"Height: {params.height} mm",
        f"Width: {params.width} mm",
        "STEP export complete",
        "Bundle generation complete",
    ]