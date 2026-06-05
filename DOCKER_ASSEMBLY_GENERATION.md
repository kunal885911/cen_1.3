# Assembly Machine - Docker Generation Instructions

## Quick Start

To generate the complete 9-part Assembly Machine STEP file, use Docker:

### Method 1: Docker Compose (Recommended)

```bash
# From project root
cd /workspaces/cen_1.3
docker-compose up --build

# Or if docker-compose is not available:
docker-compose -f backend/docker-compose.yml up --build
```

### Method 2: Direct Docker Run

```bash
# Build the image
docker build -t assembly-machine -f backend/Dockerfile .

# Run generation script
docker run -v $(pwd)/backend:/app assembly-machine \
  python generate_assembly_docker.py /app/assembly_machine.step

# Output will be in backend/assembly_machine.step
```

### Method 3: Run Inside Container

```bash
# Enter the container
docker-compose exec assembly_machine bash

# Inside container
cd /app
python generate_assembly_docker.py assembly_machine.step

# Exit and retrieve file
exit
```

## What Gets Generated

✅ **assembly_machine.step** - Complete 9-part assembly in STEP format
- Size: ~500-800 KB (depending on mesh density)
- Format: ISO-10303-21 (STEP AP203/AP214)
- Contains all 9 components in single file
- Ready for CAD import or further processing

✅ **assembly_machine_config.json** - Assembly metadata and configuration
- Component list with parameters
- Assembly positioning coordinates
- Tolerance specifications
- Material information

## System Requirements

### Minimum Requirements
- Docker or Docker Desktop installed
- 2GB available disk space
- 4GB RAM recommended

### Recommended
- 8GB RAM
- 10GB disk space
- Linux or macOS (Windows requires WSL2 or Docker Desktop)

## File Locations

After generation:
```
backend/
├── assembly_machine.step         ← Generated STEP file
├── assembly_machine_config.json  ← Configuration
├── generate_assembly_docker.py   ← Generation script
└── components/
    ├── base_plate_component.py
    ├── support_block_component.py
    ├── stepped_shaft_component.py
    ├── wheel_component.py
    ├── threaded_shaft_component.py
    ├── slotted_plate_component.py
    ├── side_block_component.py
    ├── top_plate_component.py
    └── shaft_3_component.py
```

## Viewing the Generated Assembly

### Option 1: FreeCAD (Free, Open-Source)
```bash
# On host system
freecad backend/assembly_machine.step

# Or use GUI: File > Open > assembly_machine.step
```

### Option 2: Online Viewers
- [ViewSTEP.com](https://www.viewstep.com)
- [3DViewerOnline.com](https://3dvieweronline.com)
- [Autodesk Viewer](https://viewer.autodesk.com)

Upload `assembly_machine.step` and view instantly.

### Option 3: Professional CAD Software
- Autodesk Fusion 360
- SolidWorks
- Inventor
- CATIA
- Creo

## Troubleshooting

### Docker Build Fails
```bash
# Clear cache and rebuild
docker-compose down
docker system prune -a
docker-compose up --build --no-cache
```

### Permission Denied Errors
```bash
# Fix file permissions
chmod +x backend/generate_assembly_docker.py

# Or run with sudo (not recommended)
sudo docker-compose up --build
```

### Python Module Not Found
```bash
# Rebuild without cache
docker-compose build --no-cache

# Verify Python path
docker-compose exec assembly_machine python -c "import cadquery; print('OK')"
```

### STEP Export Issues
```bash
# Check generated assembly for errors
docker-compose exec assembly_machine python -c "
from generate_assembly_docker import *
try:
    generate_assembly_machine('/tmp/test.step')
    print('SUCCESS')
except Exception as e:
    print(f'ERROR: {e}')
"
```

## Environment Variables

Set in `.env` or `docker-compose.yml`:

```env
# Component dimensions (optional overrides)
BASE_PLATE_LENGTH=500.0
BASE_PLATE_WIDTH=300.0
WHEEL_DIAMETER=250.0
ASSEMBLY_NAME=Assembly_Machine_v1
```

## Post-Generation Steps

1. **Validate Assembly**
   ```bash
   # Check STEP file integrity
   docker run -v $(pwd):/data \
     --entrypoint "python -c" \
     assembly-machine \
     "import cadquery as cq; cq.importers.importStep('/data/backend/assembly_machine.step'); print('Valid STEP file')"
   ```

2. **Convert to Other Formats**
   ```bash
   # STEP to STL
   docker run -v $(pwd):/data assembly-machine \
     python -c "
import cadquery as cq
asm = cq.importers.importStep('/data/backend/assembly_machine.step')
asm.val().exportStl('/data/backend/assembly_machine.stl')
print('Exported to STL')
"
   ```

3. **Extract Individual Components**
   ```bash
   # Use FreeCAD macro or custom Python script
   # (See documentation for component extraction)
   ```

## Performance Notes

- **Generation Time:** 30-60 seconds on modern hardware
- **Memory Usage:** 500MB - 1GB peak
- **STEP File Size:** 500-800 KB (uncompressed)
- **CPU Cores Used:** Can leverage multiple cores for boolean operations

## Docker Compose Configuration

Reference `docker-compose.yml`:
```yaml
version: '3.8'

services:
  assembly_machine:
    build:
      context: .
      dockerfile: backend/Dockerfile
    volumes:
      - ./backend:/app
    working_dir: /app
    environment:
      - PYTHONUNBUFFERED=1
    command: python generate_assembly_docker.py assembly_machine.step
```

## Customization

To modify the assembly configuration:

1. Edit `backend/schemas/assembly_machine_schema.py`:
   ```python
   schema = AssemblyMachineSchema()
   schema.wheel_outer_diameter = 280.0  # Custom size
   ```

2. Or modify `backend/configs/assembly_machine_input.json`:
   ```json
   {
     "components": [
       {
         "id": "wheel",
         "parameters": {
           "outer_diameter": 280.0
         }
       }
     ]
   }
   ```

3. Rebuild and run:
   ```bash
   docker-compose up --build
   ```

## Support & Documentation

- **Component Specs:** See `ASSEMBLY_MACHINE_GUIDE.md`
- **Engineering Drawings:** PDF format provided
- **Source Code:** Well-commented Python files in `backend/`
- **API Docs:** Inline docstrings in component classes

## Common Commands

```bash
# List running containers
docker ps

# View container logs
docker logs assembly_machine

# Execute command in container
docker exec -it assembly_machine bash

# Stop all containers
docker-compose down

# Remove all Docker data
docker system prune -a

# Update Python packages
docker-compose up --build --pull always
```

## Advanced Usage

### Custom Component Parameters
```bash
docker run -v $(pwd):/data assembly-machine python -c "
from schemas.assembly_machine_schema import AssemblyMachineSchema
from services.assembly_machine_service import AssemblyMachineService

schema = AssemblyMachineSchema()
schema.wheel_outer_diameter = 300.0
schema.base_plate_length = 600.0

service = AssemblyMachineService(schema=schema)
service.export_step('/data/custom_assembly.step')
"
```

### Batch Generation
```bash
#!/bin/bash
# Generate multiple variants
for size in 200 250 300; do
  docker-compose exec assembly_machine python -c "
from schemas.assembly_machine_schema import AssemblyMachineSchema
from services.assembly_machine_service import AssemblyMachineService

schema = AssemblyMachineSchema()
schema.wheel_outer_diameter = $size
service = AssemblyMachineService(schema=schema)
service.export_step('/app/assembly_machine_${size}mm.step')
"
done
```

---

**Last Updated:** 2026-06-05  
**Docker Version:** 20.10+ recommended  
**Python Version:** 3.10+  
**CadQuery Version:** 2.5.2+
