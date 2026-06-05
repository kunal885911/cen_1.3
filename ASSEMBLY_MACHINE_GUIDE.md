# Assembly Machine (9-Part Complex Geometry) - Implementation Guide

## Overview

This document describes the implementation of a 9-part **Assembly Machine** with complex geometry. The assembly consists of structural components, rotating mechanisms, and connector elements forming a complete mechanical assembly.

## Components Summary

| Part # | Component Name | Type | Dimensions | Key Features |
|--------|---|---|---|---|
| PART-01 | Base Plate | Foundation | 500×300×20mm | 6 mounting holes grid |
| PART-02 | Support Block (×2) | Structural | 100×100×80mm | Central bore + counterbore |
| PART-03 | Stepped Shaft | Rotating | Ø50/Ø40mm, L50 | Stepped geometry + keyway |
| PART-04 | Wheel | Rotating | Ø250mm OD, 30mm W | Bore with keyway, M8 hole |
| PART-05 | Threaded Shaft | Secondary | Ø20mm, L40mm | Flanged end, M8 thread |
| PART-06 | Slotted Plate | Connector | 350×50×20mm | 2 holes (Ø20, Ø25) |
| PART-07 | Side Block (×2) | Frame | 220×135×75mm | Step cutout, M8 bores |
| PART-08 | Top Plate | Cover | 140×100×20mm | Trapezoidal profile |
| PART-09 | Shaft 3 | Spacer | Ø25×25mm | Central bore, M8 compatible |

## File Structure

```
backend/
├── components/
│   ├── base_plate_component.py
│   ├── support_block_component.py
│   ├── stepped_shaft_component.py
│   ├── wheel_component.py
│   ├── threaded_shaft_component.py
│   ├── slotted_plate_component.py
│   ├── side_block_component.py
│   ├── top_plate_component.py
│   └── shaft_3_component.py          # NEW
├── schemas/
│   └── assembly_machine_schema.py    # NEW
├── services/
│   └── assembly_machine_service.py   # NEW
├── configs/
│   └── assembly_machine_input.json   # NEW
├── generate_assembly_machine.py      # NEW
└── generate_assembly_docker.py       # NEW
```

## Key Features

### 1. Component Architecture
- Each part is a `BaseComponent` subclass
- Follows consistent interface: `generate()` and `get_connectors()`
- Fully parameterized for easy configuration
- All edges chamfered 0.5×45° per engineering standard

### 2. Assembly Schema
- Centralized configuration in `AssemblyMachineSchema` dataclass
- Defines all component parameters and positions
- Supports custom positioning and rotation
- JSON export for documentation

### 3. Assembly Service
- `AssemblyMachineService` orchestrates component creation
- Automatic positioning and alignment
- Union/boolean operations for assembly
- STEP file export

### 4. Assembly Logic

**Hierarchy:**
```
Base Plate (Z=0)
├── Support Block Front (Z=20)
├── Support Block Back (Z=20)
├── Side Block Left (Z=100)
├── Side Block Right (Z=100)
├── Top Plate (Z=180)
├── Stepped Shaft + Wheel (Z=80-100)
├── Threaded Shaft (Z=100)
├── Slotted Plate (Z=50)
└── Shaft 3 (Z=130)
```

**Key Connections:**
- Support blocks mount on base plate mounting holes
- Side blocks mount on support blocks (vertical frame)
- Top plate covers the frame assembly
- Stepped shaft rotates through wheel (main mechanism)
- Slotted plate acts as vertical connector
- Shaft 3 spacer bridges between assemblies

## Usage

### Option 1: Direct Python (Recommended for Docker)

```bash
cd backend

# Using Docker-optimized version
python generate_assembly_docker.py assembly_machine.step

# Using service-based version (requires OCP/OpenGL)
python generate_assembly_machine.py assembly_machine.step
```

### Option 2: Within Docker Container

```bash
# Build and run with Docker Compose
docker-compose up --build

# Or manually:
docker build -t assembly-machine -f backend/Dockerfile .
docker run -v $(pwd)/backend:/app assembly-machine python generate_assembly_docker.py /app/assembly_machine.step
```

### Option 3: Programmatic Usage

```python
from services.assembly_machine_service import AssemblyMachineService
from schemas.assembly_machine_schema import AssemblyMachineSchema

# Create custom configuration
schema = AssemblyMachineSchema()
schema.wheel_outer_diameter = 280.0  # Custom size
schema.base_plate_length = 600.0

# Generate assembly
service = AssemblyMachineService(schema=schema)
assembly = service.assemble()
service.export_step("my_assembly.step")
```

## Component Specifications

### PART-01: Base Plate
- **Dimensions:** 500L × 300W × 20H mm
- **Holes:** 6× Ø9mm (3×2 grid)
- **Hole Positions:** X=40, 220, 410; Y=85, 215 (from bottom-left)
- **Material:** Steel
- **Purpose:** Foundation for entire assembly

### PART-02: Support Block (Qty 2)
- **Dimensions:** 100L × 100W × 80H mm
- **Bore:** Central Ø14mm with Ø20mm counterbore (12.6mm deep)
- **Mounting:** 2× Ø9mm holes (at X=10,90; Y=10,90)
- **Purpose:** Vertical support elements

### PART-03: Stepped Shaft
- **Main Section:** Ø50mm, 20mm length
- **Shoulder Section:** Ø40mm, 30mm length
- **Total Length:** 50mm
- **Keyway:** 10mm wide, from Z=27.9 to Z=50
- **Purpose:** Central rotating axis

### PART-04: Wheel
- **Outer Diameter:** 250mm
- **Width:** 30mm
- **Central Bore:** Ø40mm
- **Keyway:** 10mm wide, 4.5mm height at bottom
- **M8 Hole:** At Y=100mm from center
- **Purpose:** Rotating mechanism

### PART-05: Threaded Shaft
- **Main Diameter:** 20mm
- **Main Length:** 35mm
- **Flange:** 30mm diameter × 5mm thick
- **M8 Thread:** 6.8mm tap drill, 15mm deep
- **Total Length:** 40mm
- **Purpose:** Secondary rotating element with threaded interface

### PART-06: Slotted Plate
- **Dimensions:** 350L × 50W × 20H mm
- **Bottom Hole:** Ø20mm (25mm from edge)
- **Top Hole:** Ø25mm (25mm from opposite edge)
- **Purpose:** Vertical connector linking structural elements

### PART-07: Side Block (Qty 2)
- **Dimensions:** 220L × 135W (height) × 75W (depth) mm
- **Step Cutout:** Top-front edge (30mm wide, 20mm tall)
- **M8 Bores:** 2× at bottom (33.8mm depth, 25mm from back)
- **Purpose:** Main frame left and right elements

### PART-08: Top Plate
- **Dimensions:** 140L × 100W × 20H mm
- **Profile:** Trapezoidal (45° slanted right edge)
- **Top Width:** 80mm (20mm less than base)
- **Hole:** Ø9mm, 20mm from left edge
- **Purpose:** Top cover with slanted face

### PART-09: Shaft 3
- **Outer Diameter:** 25mm ±0.01mm
- **Length:** 25mm
- **Central Bore:** 8mm (M8 compatible)
- **Purpose:** Cylindrical spacer for alignment

## Assembly Views

The assembly is designed to be viewed from:
- **Front:** Shows main vertical structure with central void
- **Side:** Reveals wheel on rotating shaft mechanism
- **Top:** Shows base layout and component arrangement
- **Isometric:** 3D visualization of complete assembly

## Tolerance Standards

- **Basis:** ISO metric system
- **General Tolerance:** ±1mm
- **Precision Tolerance:** ±0.1mm
- **High Precision:** ±0.01mm
- **Angular:** ±0.1°
- **Edge Chamfer:** 0.5×45° (all unspecified edges)

## Material Specifications

- **Default Material:** Steel
- **Surface Finish:** As machined
- **Heat Treatment:** None (unless specified)
- **Coating:** None (unless specified)

## Export Formats

The assembly can be exported as:
- **STEP** (.step) - Full 3D CAD model
- **JSON** (.json) - Configuration and metadata
- **Individual Components:** STL or STEP format

## Validation Checklist

- [ ] All 9 components created successfully
- [ ] Components positioned correctly
- [ ] No interference between parts
- [ ] All holes and bores align correctly
- [ ] Keywayfeatures match interface requirements
- [ ] STEP file exports without errors
- [ ] Visual inspection confirms geometry
- [ ] Assembly matches engineering drawings

## Troubleshooting

### OpenGL/Graphics Error
**Issue:** `ImportError: libGL.so.1: cannot open shared object file`

**Solution:** Run in Docker container where graphics libraries are properly installed:
```bash
docker-compose up --build
```

Or use the headless-friendly Docker version:
```bash
python generate_assembly_docker.py assembly_machine.step
```

### Component Positioning Issues
**Issue:** Parts overlapping or misaligned

**Solution:** Check `AssemblyMachineSchema` class positioning parameters:
```python
schema = AssemblyMachineSchema()
# Adjust positioning as needed
schema.support_block_front_position = (-200, -100, 20)
```

### Export Failures
**Issue:** STEP file generation fails

**Solution:** Ensure all components are valid solids:
```python
service = AssemblyMachineService()
service.create_all_components()
for name, component in service.components.items():
    print(f"{name}: {component.val()}")
```

## Next Steps

1. **Validate Geometry:**
   - Import STEP file in CAD software (FreeCAD, SolidWorks, etc.)
   - Compare with reference assembly drawings
   - Verify all dimensions and tolerances

2. **Customize Assembly:**
   - Modify parameters in `AssemblyMachineSchema`
   - Create variant configurations
   - Support multiple sizes or material options

3. **Manufacturing Integration:**
   - Generate individual component drawings
   - Create manufacturing sequence documents
   - Define assembly work instructions

4. **Further Development:**
   - Add surface finish specifications
   - Implement material properties
   - Create assembly animations
   - Generate BOM (Bill of Materials)

## References

- Engineering Drawings: Provided in PDF format (top/front/side views)
- Component Code: Implemented in `backend/components/`
- API Documentation: See docstrings in source files

## Support

For questions or issues:
1. Check component code in `backend/components/`
2. Review assembly configuration in `backend/configs/assembly_machine_input.json`
3. Consult engineering drawings and design specifications
4. Run tests to validate assembly: `python -m pytest tests/`

---

**Document Version:** 1.0  
**Last Updated:** 2026-06-05  
**Assembly Name:** Assembly Machine  
**Total Components:** 9  
**Design Status:** Complete
