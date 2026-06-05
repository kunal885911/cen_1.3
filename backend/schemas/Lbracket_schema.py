from pydantic import BaseModel, Field, model_validator


class LbracketParams(BaseModel):
    length_1: float = Field(ge=10, le=1000)
    length_2: float = Field(ge=10, le=1000)
    width: float = Field(ge=10, le=500)

    @model_validator(mode='after')
    def validate_l_bracket(self) -> 'LbracketParams':
        # Ensure arm lengths are proportional to width
        if self.length_1 < self.width or self.length_2 < self.width:
            raise ValueError("Geometry Failure: Arm lengths must be >= Width (B).")
        return self