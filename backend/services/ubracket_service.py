from core.generator import generate_model_bundle
from cad.brackets.ubracket_generator import generate_ubracket_step_file
from cad.brackets.ubracket_log import ubracket_logs


from schemas.ubracket_schema import UbracketParams

async def generate_Ubracket(params: UbracketParams) -> dict[str, object]:
    
    return await generate_model_bundle(
        model_name="ubracket",
        params=params,
        step_generator=generate_ubracket_step_file,
        log_builder=ubracket_logs,
    )
