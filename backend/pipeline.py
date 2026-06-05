import os
import uuid
import json
from datetime import datetime, timezone
from pathlib import Path

from config.loader import ConfigLoader
from config.factory import ComponentFactory
from assembly.assembler import Assembler
from services.file_service import GENERATED_FILES_DIR
from zipfile import ZIP_DEFLATED, ZipFile

class CADPipeline:
    """
    Config-driven pipeline for CAD generation and assembly.
    Orchestrates loading configuration, component instantiation, and assembly.
    """
    def __init__(self):
        self.loader = ConfigLoader()
        self.factory = ComponentFactory()
        self.assembler = Assembler()

    def run_from_file(self, config_path: str) -> dict:
        """
        Full pipeline: load → validate → generate parts → validate connectors
        → assemble → export → return result summary.
        Prints step-by-step status log to stdout.
        """
        print(f"[CADPipeline] Starting pipeline for file: {config_path}")
        path_obj = Path(config_path)
        
        # 1. Load config
        if path_obj.suffix.lower() in [".yaml", ".yml"]:
            print("[CADPipeline] Loading YAML configuration...")
            config_dict = self.loader.load_yaml(config_path)
        else:
            print("[CADPipeline] Loading JSON configuration...")
            config_dict = self.loader.load_json(config_path)
            
        return self.run_from_dict(config_dict)

    def run_from_dict(self, config: dict) -> dict:
        """Same pipeline, accepts a parsed dict instead of a file path."""
        print("[CADPipeline] Validating configuration...")
        
        # 2. Validate config
        # This will cascade down to the existing per-model Pydantic schemas.
        assembly_req = self.loader.validate(config)
        
        print(f"[CADPipeline] Generating {len(assembly_req.parts)} parts...")
        # 3. Generate parts using the factory
        parts = {}
        for part_cfg in assembly_req.parts:
            # The factory uses the type string to create the respective component,
            # applying schema validation rules again before instantiation for safety.
            parts[part_cfg.id] = self.factory.create(part_cfg.type, **part_cfg.parameters)
            
        print(f"[CADPipeline] Assembling {len(assembly_req.connections)} connections...")
        # 4. Assemble
        self.assembler.assemble(parts, assembly_req.connections)
        
        # 5. Export
        print("[CADPipeline] Exporting assemblies...")
        job_id = uuid.uuid4().hex
        bundle_dir = GENERATED_FILES_DIR / f"pipeline-{job_id}"
        bundle_dir.mkdir(parents=True, exist_ok=True)
        
        self.assembler.export_step(str(bundle_dir))
            
        metadata = {
            "model_type": "pipeline_assembly",
            "assembly_name": assembly_req.assembly_name,
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }
        (bundle_dir / "metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
        (bundle_dir / "params.json").write_text(assembly_req.model_dump_json(indent=2), encoding="utf-8")
        
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
        
        logs = [f"Pipeline Assembly '{assembly_req.assembly_name}' generated successfully."]
        logs.append(f"Parts generated: {len(parts)}")
        logs.append(f"Connections applied: {len(assembly_req.connections)}")
        if hasattr(self.assembler, "assembly_log"):
            logs.extend(self.assembler.assembly_log)
        (bundle_dir / "logs.txt").write_text("\n".join(logs) + "\n", encoding="utf-8")
        
        zip_filename = f"pipeline-output-{job_id}.zip"
        zip_path = GENERATED_FILES_DIR / zip_filename
        
        print("[CADPipeline] Packaging ZIP file...")
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
                
        print(f"[CADPipeline] Finished. Outputs saved to {zip_filename}")
        
        return {
            "success": True,
            "message": "Pipeline assembly generated successfully",
            "fileUrl": f"/api/download/{zip_filename}",
            "downloadName": "assembly-output.zip",
            "outputFiles": step_files + ["params.json", "metadata.json", "logs.txt", "color_legend.json"]
        }
