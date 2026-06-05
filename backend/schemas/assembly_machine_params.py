from pydantic import BaseModel, Field
from typing import Optional

class AssemblyMachineParams(BaseModel):
    """Parameters for Assembly Machine generation"""
    base_plate_length: float = Field(default=500.0, description="Base plate length in mm")
    base_plate_width: float = Field(default=300.0, description="Base plate width in mm")
    wheel_diameter: float = Field(default=250.0, description="Wheel outer diameter in mm")
    name: str = Field(default="assembly_machine", description="Assembly name")
