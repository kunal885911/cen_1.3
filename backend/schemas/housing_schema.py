from pydantic import BaseModel, Field, model_validator


class HousingParams(BaseModel):
    length: float = Field(ge=20, le=2000)
    height: float = Field(ge=20, le=2000)
    width: float = Field(ge=20, le=2000)

    @model_validator(mode='after')
    def validate_housing_cavity(self) -> 'HousingParams':
        # Ensure the 6mm walls (12mm total) don't consume more than 40% of the side
        min_side = min(self.length, self.height, self.width)
        derived_wall = max(6.0, (0.1 * min_side) + 7.5)
        if derived_wall >= (min_side * 0.4):
            raise ValueError("Geometry Failure: Internal dimensions are too small to accommodate required wall thickness.")
        return self