from pydantic import BaseModel, Field, model_validator


class PlateParams(BaseModel):
    length: float = Field(ge=10, le=2000)
    width: float = Field(ge=10, le=2000)

    @model_validator(mode='after')
    def validate_plate_proportions(self) -> 'PlateParams':
        # Reject if L > 4W (Simulation safety rail)
        if self.length > (self.width * 4):
            raise ValueError("Geometry Failure: Plate aspect ratio (L/W) must be 4:1 or less.")
        return self