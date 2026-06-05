from pydantic import BaseModel
from typing import Literal

class ConnectorSchema(BaseModel):
    position: tuple[float, float, float]
    axis: tuple[float, float, float]
    type: Literal["cylindrical", "face", "hole"]
    diameter: float | None = None
    compatibility: list[str]

class ConnectionSchema(BaseModel):
    part_a: str
    conn_a: str
    part_b: str
    conn_b: str
