from pydantic import BaseModel, model_validator
from typing import Any

# Import existing schemas to delegate parameter validation
from schemas.shaft_schema import ShaftParams
from schemas.flange_schema import FlangeParams
from schemas.plate_schema import PlateParams
from schemas.Lbracket_schema import LbracketParams
from schemas.ubracket_schema import UbracketParams
from schemas.housing_schema import HousingParams

SCHEMA_MAP = {
    "shaft": ShaftParams,
    "flange": FlangeParams,
    "plate": PlateParams,
    "lbracket": LbracketParams,
    "ubracket": UbracketParams,
    "housing": HousingParams
}

class PartConfig(BaseModel):
    id: str
    type: str   # "shaft", "flange", "plate", "lbracket", "ubracket", "housing"
    parameters: dict

    @model_validator(mode="after")
    def validate_parameters(self):
        """
        Delegate to the existing per-model Pydantic schema for parameter validation.
        E.g. if type=="shaft", instantiate ShaftParams(**self.parameters).
        This reuses ALL existing validation rules (L<=20xD, etc.) automatically.
        
        Detailed Explanation:
        By utilizing the existing schema classes, any validation error defined
        for individual components will be raised here, meaning we do not duplicate
        any logic. It enforces the exact same rules as the individual generation endpoints.
        """
        if self.type not in SCHEMA_MAP:
            raise ValueError(f"Unknown part type: {self.type}")
        
        schema_class = SCHEMA_MAP[self.type]
        # This will raise a ValidationError if parameters are invalid
        schema_class(**self.parameters)
        return self

class AssemblyRequest(BaseModel):
    assembly_name: str
    parts: list[PartConfig]
    connections: list[tuple[str, str]]   # [("shaft1.right_end", "flange1.back_center")]
    export_modes: list[str] = ["assembly"]  # subset of ["assembly","multibody","individual"]
