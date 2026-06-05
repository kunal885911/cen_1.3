from uuid import uuid4
from services.file_service import GENERATED_FILES_DIR
import asyncio
from concurrent.futures import ProcessPoolExecutor
from zipfile import ZIP_DEFLATED, ZipFile
import json
from datetime import datetime, timezone

executor = ProcessPoolExecutor()

async def generate_model_bundle(*, model_name: str, params, log_builder, step_generator) -> dict[str, object]:

    job_id = uuid4().hex
    bundle_dir = GENERATED_FILES_DIR / f"{model_name}-{job_id}"
    bundle_dir.mkdir(parents=True, exist_ok=True)

    #generating step_file path 
    step_filename = f"{model_name}.step"
    step_path = bundle_dir / step_filename

    #generating params.json file path
    params_filename = "params.json"
    params_path = bundle_dir / params_filename

    #generating metadata.json file path
    metadata_filename = "metadata.json"
    metadata_path = bundle_dir / metadata_filename

    #generating log.txt file path
    logs_filename = "logs.txt"
    logs_path = bundle_dir / logs_filename

    #converting params into dict
    params_dict = params.model_dump()

    #processpool part implementation
    loop = asyncio.get_running_loop()
    await loop.run_in_executor( executor, step_generator, params_dict, str(step_path))

    params_path.write_text(params.model_dump_json(indent=2), encoding="utf-8")

    # Metadata
    metadata = {
        "model_type": model_name,
        "unit": "mm",
        "engine": "CadQuery",
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }
    metadata_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    # Logs (dynamic)
    logs = log_builder(params)
    logs_path.write_text("\n".join(logs) + "\n", encoding="utf-8")

    # ZIP
    zip_filename = f"{model_name}-output-{job_id}.zip"
    zip_path = GENERATED_FILES_DIR / zip_filename

    with ZipFile(zip_path, mode="w", compression=ZIP_DEFLATED) as archive:
        for file in [params_filename, metadata_filename, logs_filename]:
            archive.write(bundle_dir / file, arcname=file)
            
        # Add all generated .step files to the archive
        step_files = []
        for step_file in bundle_dir.glob("*.step"):
            archive.write(step_file, arcname=step_file.name)
            step_files.append(step_file.name)
            
    return {
        "download_filename": zip_filename,
        "download_name": f"{model_name}-output.zip",
        "message": f"{model_name} generated successfully",
        "output_files": step_files + [params_filename, metadata_filename, logs_filename],
    }