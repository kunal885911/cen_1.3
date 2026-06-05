#!/usr/bin/env python3
"""
Assembly Machine Generator

Generates a 9-part assembly machine STEP file using CadQuery.
The assembly consists of:
- PART-01: Base Plate (500×300×20mm)
- PART-02: Support Blocks x2 (100×100×80mm each)
- PART-03: Stepped Shaft (50mm assembly)
- PART-04: Wheel (250mm OD)
- PART-05: Threaded Shaft (20mm with flange)
- PART-06: Slotted Plate (350×50×20mm)
- PART-07: Side Blocks x2 (220×135×75mm each)
- PART-08: Top Plate (140×100×20mm trapezoidal)
- PART-09: Shaft 3 (25mm cylindrical spacer)

Usage:
    python generate_assembly_machine.py [output_path]
    
Example:
    python generate_assembly_machine.py assembly_machine.step
"""

import sys
import os
import json

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Import directly to avoid __init__.py conflicts
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'services'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'schemas'))

from assembly_machine_service import AssemblyMachineService
from assembly_machine_schema import AssemblyMachineSchema


def generate_assembly(output_file: str = "assembly_machine.step") -> None:
    """Generate the assembly machine and export to STEP file"""
    
    print("=" * 70)
    print("ASSEMBLY MACHINE GENERATOR")
    print("=" * 70)
    print("\nInitializing assembly machine service...")
    
    # Create schema and service
    schema = AssemblyMachineSchema()
    service = AssemblyMachineService(schema=schema)
    
    # Get assembly info
    info = service.get_assembly_info()
    print(f"\nAssembly: {info['name']}")
    print(f"Total Parts: {info['parts_count']}")
    print("\nComponents:")
    for comp_name, part_num in info['components'].items():
        print(f"  - {comp_name}: {part_num}")
    
    print("\nGenerating components...")
    service.create_all_components()
    print("✓ All 9 components created successfully")
    
    print("\nPositioning components...")
    positioned = service.position_components()
    print("✓ Components positioned")
    
    print("\nAssembling...")
    assembly = service.assemble()
    print("✓ Assembly complete")
    
    print(f"\nExporting to STEP file: {output_file}")
    service.export_step(output_file)
    
    print("\n" + "=" * 70)
    print("✓ ASSEMBLY GENERATION COMPLETE")
    print("=" * 70)
    print(f"\nOutput file: {output_file}")
    print(f"File size: {os.path.getsize(output_file) / 1024:.2f} KB")
    
    # Save assembly configuration as JSON for reference
    config_file = output_file.replace('.step', '_config.json')
    with open(config_file, 'w') as f:
        json.dump(info, f, indent=2)
    print(f"Configuration saved: {config_file}")


if __name__ == "__main__":
    output_file = sys.argv[1] if len(sys.argv) > 1 else "assembly_machine.step"
    
    try:
        generate_assembly(output_file)
    except Exception as e:
        print(f"\n✗ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
