from pydantic import BaseModel, Field, model_validator


class ShaftParams(BaseModel):
    diameter: float = Field(ge=6, le=500)
    length: float = Field(ge=10, le=2000)

    @model_validator(mode='after')
    def validate_shaft_stability(self) -> 'ShaftParams':
        # Reject if L > 20d (Stability safety rail)
        if self.length > (self.diameter * 20):
            raise ValueError(f"Geometry Failure: Shaft length ({self.length}mm) cannot exceed 20x diameter ({self.diameter}mm).")
        return self
