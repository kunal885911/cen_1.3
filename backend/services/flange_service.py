from core.generator import generate_model_bundle
from cad.flange.generator import generate_flange_step_file
from cad.flange.log import flange_logs

from schemas.flange_schema import FlangeParams

    
async def generate_flange(params: FlangeParams) -> dict[str, object]:
    return await generate_model_bundle(
        model_name="flange",
        params=params,
        step_generator=generate_flange_step_file, 
        log_builder=flange_logs
    )
