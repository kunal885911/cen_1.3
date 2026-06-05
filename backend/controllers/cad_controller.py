from pathlib import Path

from fastapi import APIRouter, HTTPException, status, UploadFile, File
from fastapi.responses import FileResponse
from pydantic import ValidationError

from schemas.generate_schema import GenerateRequest, GenerateResponse
from schemas.plate_schema import PlateParams
from schemas.shaft_schema import ShaftParams
from schemas.Lbracket_schema import LbracketParams
from schemas.ubracket_schema import UbracketParams
from schemas.flange_schema import FlangeParams
from schemas.housing_schema import HousingParams
from services.file_service import get_output_file_path
from services.plate_service import generate_plate
from services.shaft_service import generate_shaft
from services.flange_service import generate_flange
from services.Lbracket_service import generate_Lbracket
from services.ubracket_service import generate_Ubracket
from services.housing_service import generate_housing
from services.file_service import get_output_file_path, GENERATED_FILES_DIR

import uuid
import json
from datetime import datetime, timezone
from zipfile import ZIP_DEFLATED, ZipFile

from schemas.assembly_schema import AssemblyRequest
from assembly.assembler import Assembler

from components.shaft_component import ShaftComponent
from components.flange_component import FlangeComponent
from components.plate_component import PlateComponent
from components.lbracket_component import LBracketComponent
from components.ubracket_component import UBracketComponent
from components.housing_component import HousingComponent

COMPONENT_MAPPING = {
    "shaft": ShaftComponent,
    "flange": FlangeComponent,
    "plate": PlateComponent,
    "lbracket": LBracketComponent,
    "ubracket": UBracketComponent,
    "housing": HousingComponent
}


router = APIRouter(prefix="/api", tags=["cad"])


async def _process_cad_generation(generate_func, params) -> GenerateResponse:
    try:
        generation_result = await generate_func(params)
    except ValidationError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "success": False,
                "message": "Failed to generate CAD file",
                "error": str(exc),
            },
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "success": False,
                "message": "Failed to generate CAD file",
                "error": str(exc),
            },
        ) from exc

    return GenerateResponse(
        success=True,
        message=str(generation_result["message"]),
        fileUrl=f"/api/download/{generation_result['download_filename']}",
        downloadName=str(generation_result["download_name"]),
        outputFiles=[str(item) for item in generation_result["output_files"]],
    )


@router.post("/shaft/generate", response_model=GenerateResponse, status_code=status.HTTP_200_OK)
async def generate_shaft_cad(params: ShaftParams) -> GenerateResponse:
    return await _process_cad_generation(generate_shaft, params)

@router.post("/flange/generate", response_model=GenerateResponse, status_code=status.HTTP_200_OK)
async def generate_flange_cad(params: FlangeParams) -> GenerateResponse:
    return await _process_cad_generation(generate_flange, params)

@router.post("/ubracket/generate", response_model=GenerateResponse, status_code=status.HTTP_200_OK)
async def generate_Ubracket_cad(params: UbracketParams) -> GenerateResponse:
    return await _process_cad_generation(generate_Ubracket, params)

@router.post("/lbracket/generate", response_model=GenerateResponse, status_code=status.HTTP_200_OK)
async def generate_Lbracket_cad(params: LbracketParams) -> GenerateResponse:
    return await _process_cad_generation(generate_Lbracket, params)

@router.post("/housing/generate", response_model=GenerateResponse, status_code=status.HTTP_200_OK)
async def generate_housing_cad(params: HousingParams) -> GenerateResponse:
    return await _process_cad_generation(generate_housing, params)

@router.post("/plate/generate", response_model=GenerateResponse, status_code=status.HTTP_200_OK)
async def generate_plate_cad(params: PlateParams) -> GenerateResponse:
    return await _process_cad_generation(generate_plate, params)


@router.post("/assembly/generate", response_model=GenerateResponse, status_code=status.HTTP_200_OK)
async def generate_assembly(request: AssemblyRequest) -> GenerateResponse:
    print(f"[DEBUG] Incoming Assembly Request connections: {request.connections}")
    """
    1. Validate all part parameters via existing per-model schemas (reused inside PartConfig)
    2. Instantiate component objects via ComponentFactory mapping
    3. Run Assembler.assemble(parts, connections)
    4. Run Assembler.export_step() for each requested mode
    5. Package output into ZIP using existing services/ packaging logic
    6. Return same response format as existing endpoints
    """
    try:
        parts = {}
        for part in request.parts:
            CompClass = COMPONENT_MAPPING[part.type]
            parts[part.id] = CompClass(**part.parameters)
            
        assembler = Assembler()
        assembler.assemble(parts, request.connections)
        
        job_id = uuid.uuid4().hex
        bundle_dir = GENERATED_FILES_DIR / f"assembly-{job_id}"
        bundle_dir.mkdir(parents=True, exist_ok=True)
        
        assembler.export_step(str(bundle_dir))
            
        metadata = {
            "model_type": "assembly",
            "assembly_name": request.assembly_name,
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }
        (bundle_dir / "metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
        (bundle_dir / "params.json").write_text(request.model_dump_json(indent=2), encoding="utf-8")
        
        from components.color_registry import get_color
        color_legend = {}
        for part_id, comp in parts.items():
            color_data = get_color(comp.component_type)
            color_legend[part_id] = {
                "type": comp.component_type,
                "color_name": color_data["name"],
                "rgb": [color_data["r"], color_data["g"], color_data["b"]]
            }
        (bundle_dir / "color_legend.json").write_text(json.dumps(color_legend, indent=2), encoding="utf-8")
        
        logs = [f"Assembly '{request.assembly_name}' generated successfully."]
        logs.append(f"Parts generated: {len(parts)}")
        logs.append(f"Connections applied: {len(request.connections)}")
        (bundle_dir / "logs.txt").write_text("\n".join(logs) + "\n", encoding="utf-8")
        
        zip_filename = f"assembly-output-{job_id}.zip"
        zip_path = GENERATED_FILES_DIR / zip_filename
        
        with ZipFile(zip_path, mode="w", compression=ZIP_DEFLATED) as archive:
            for file in ["params.json", "metadata.json", "logs.txt", "color_legend.json"]:
                archive.write(bundle_dir / file, arcname=file)
                
            step_files = []
            for step_file in bundle_dir.rglob("*.step"):
                if step_file.parent.name == "individual":
                    arc_name = f"part_{step_file.name}"
                else:
                    arc_name = step_file.name
                archive.write(step_file, arcname=arc_name)
                step_files.append(arc_name)
                
        return GenerateResponse(
            success=True,
            message="Assembly generated successfully",
            fileUrl=f"/api/download/{zip_filename}",
            downloadName="assembly-output.zip",
            outputFiles=step_files + ["params.json", "metadata.json", "logs.txt", "color_legend.json"],
        )
        
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "success": False,
                "message": "Failed to generate Assembly",
                "error": str(exc),
            },
        ) from exc


@router.get("/download/{filename}")
def download_cad_file(filename: str) -> FileResponse:
    # Basic safety guard against path traversal.
    if "/" in filename or "\\" in filename:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid filename")

    file_path = get_output_file_path(filename)
    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")

    return FileResponse(
        path=file_path,
        media_type="application/zip",
        filename=Path(filename).name,
    )


@router.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}

from pipeline import CADPipeline
import tempfile

@router.post("/assembly/config", response_model=GenerateResponse, status_code=status.HTTP_200_OK)
async def assembly_from_config(file: UploadFile = File(...)):
    """
    Accept a JSON or YAML config file upload.
    Run CADPipeline.run_from_file() on the uploaded file.
    Return same response format as /api/assembly/generate.
    """
    try:
        # Create a temporary file to save the uploaded config
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name

        pipeline = CADPipeline()
        result = pipeline.run_from_file(tmp_path)
        
        # Clean up the temporary file
        Path(tmp_path).unlink(missing_ok=True)
        
        return GenerateResponse(**result)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "success": False,
                "message": "Failed to generate Assembly from config",
                "error": str(exc),
            },
        ) from exc
