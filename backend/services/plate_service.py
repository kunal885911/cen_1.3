from core.generator import generate_model_bundle
from cad.plate.generator import generate_plate_step_file
from cad.plate.log import plate_logs

from schemas.plate_schema import PlateParams


async def generate_plate(params: PlateParams) -> dict[str, object]:

    return await generate_model_bundle(
        model_name="plate",
        params=params,
        step_generator=generate_plate_step_file,
        log_builder=plate_logs,
    )
