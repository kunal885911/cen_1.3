from core.generator import generate_model_bundle
from cad.shaft.generator import generate_shaft_step_file
from cad.shaft.log import shaft_logs

from schemas.shaft_schema import ShaftParams
    
async def generate_shaft(params: ShaftParams) -> dict[str, object]:
    
    return await generate_model_bundle(
        model_name="shaft",
        params=params,
        step_generator=generate_shaft_step_file,
        log_builder=shaft_logs,
    )
