from typing import Any, Literal
from typing import Optional, List

from pydantic import BaseModel, Field


class GenerateRequest(BaseModel):
    type: Literal["shaft", "plate", "flange", "lbracket", "ubracket", "housing"]
    params: dict[str, Any] = Field(default_factory=dict)


class GenerateResponse(BaseModel):
    success: bool
    message: str
    fileUrl: Optional[str] = None
    downloadName: Optional[str] = None
    outputFiles: Optional[List[str]] = None
    error: Optional[str] = None
