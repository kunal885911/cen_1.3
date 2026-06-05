from pydantic import BaseModel, Field


class FlangeParams(BaseModel):
    inner_diameter: float = Field(ge=36, le=620)