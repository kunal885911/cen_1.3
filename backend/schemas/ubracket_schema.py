from pydantic import BaseModel, Field, model_validator


class UbracketParams(BaseModel):
    length: float = Field(ge=10, le=1000)
    height: float = Field(ge=10, le=1000)
    width: float = Field(ge=10, le=500)

    @model_validator(mode='after')
    def validate_u_bracket(self) -> 'UbracketParams':
        if self.length < self.width or self.height < self.width:
            raise ValueError("Geometry Failure: Base length and height must be >= Width (B).")
        return self