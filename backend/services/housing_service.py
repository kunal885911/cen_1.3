from core.generator import generate_model_bundle
from cad.housing.generator import generate_housing_step_file
from cad.housing.log import housing_logs


from schemas.housing_schema import HousingParams

async def generate_housing(params: HousingParams) -> dict[str, object]:

    return await generate_model_bundle(
        model_name="housing",
        params=params,
        step_generator=generate_housing_step_file,
        log_builder=housing_logs,
    )
