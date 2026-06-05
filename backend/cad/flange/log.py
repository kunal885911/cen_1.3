from schemas.flange_schema import FlangeParams
def flange_logs(params: FlangeParams):
    return [
        "Process started",
        "Model type: flange",
        f"Inner_Diameter: {params.inner_diameter} mm",
        "STEP export complete",
        "Bundle generation complete",
    ]