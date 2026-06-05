from core.generator import generate_model_bundle
from cad.brackets.lbracket_generator import generate_lbracket_step_file
from cad.brackets.lbracket_log import lbracket_logs

from schemas.Lbracket_schema import LbracketParams

    
async def generate_Lbracket(params: LbracketParams) -> dict[str, object]:
    
    return await generate_model_bundle(
        model_name="lbracket",
        params=params,
        step_generator=generate_lbracket_step_file,
        log_builder=lbracket_logs,
    )
