#!/usr/bin/env python3
"""
Assembly Machine STEP Generator (Docker version)

This script generates the complete 9-part assembly machine and exports it as a STEP file.
It should be run inside the Docker container where all dependencies are properly configured.

Run with: docker-compose up --build
Or: docker run -v $(pwd):/app assembly_machine_generator
"""

import sys
import os
import json
import cadquery as cq
from typing import Dict, List

# Component definitions
class ComponentRegistry:
    """Registry of all 9 assembly machine components"""
    
    PART_01_BASE_PLATE = {
        "name": "Base Plate",
        "type": "base_plate",
        "params": {
            "length": 500.0,
            "width": 300.0,
            "height": 20.0
        }
    }
    
    PART_02_SUPPORT_BLOCK = {
        "name": "Support Block",
        "type": "support_block",
        "params": {
            "length": 100.0,
            "width": 100.0,
            "height": 80.0
        }
    }
    
    PART_03_STEPPED_SHAFT = {
        "name": "Stepped Shaft",
        "type": "stepped_shaft",
        "params": {
            "diameter": 50.0,
            "length": 50.0,
            "shoulder_diameter": 40.0,
            "shoulder_length": 20.0
        }
    }
    
    PART_04_WHEEL = {
        "name": "Wheel",
        "type": "wheel",
        "params": {
            "outer_diameter": 250.0,
            "width": 30.0,
            "bore_diameter": 40.0
        }
    }
    
    PART_05_THREADED_SHAFT = {
        "name": "Threaded Shaft",
        "type": "threaded_shaft",
        "params": {
            "diameter": 20.0,
            "length": 40.0
        }
    }
    
    PART_06_SLOTTED_PLATE = {
        "name": "Slotted Plate",
        "type": "slotted_plate",
        "params": {
            "length": 350.0,
            "width": 50.0,
            "height": 20.0
        }
    }
    
    PART_07_SIDE_BLOCK = {
        "name": "Side Block",
        "type": "side_block",
        "params": {
            "length": 220.0,
            "width": 135.0,
            "height": 75.0
        }
    }
    
    PART_08_TOP_PLATE = {
        "name": "Top Plate",
        "type": "top_plate",
        "params": {
            "length": 140.0,
            "width": 100.0,
            "height": 20.0
        }
    }
    
    PART_09_SHAFT_3 = {
        "name": "Shaft 3",
        "type": "shaft_3",
        "params": {
            "outer_diameter": 25.0,
            "length": 25.0,
            "bore_diameter": 8.0
        }
    }


class AssemblyMachineBuilder:
    """Builder class for assembly machine components"""
    
    @staticmethod
    def create_base_plate(params: Dict) -> cq.Workplane:
        """Create PART-01: Base Plate"""
        L = params.get("length", 500.0)
        W = params.get("width", 300.0)
        H = params.get("height", 20.0)
        
        plate = cq.Workplane("XY").box(L, W, H)
        
        # Hole positions
        xs = [-L/2 + 40, -L/2 + 220, -L/2 + 410]
        ys = [-W/2 + 85, -W/2 + 215]
        pts = [(x, y) for x in xs for y in ys]
        
        plate = plate.faces(">Z").workplane().pushPoints(pts).hole(9.0)
        plate = plate.edges().chamfer(0.5)
        
        return plate
    
    @staticmethod
    def create_support_block(params: Dict) -> cq.Workplane:
        """Create PART-02: Support Block"""
        L = params.get("length", 100.0)
        W = params.get("width", 100.0)
        H = params.get("height", 80.0)
        
        block = cq.Workplane("XY").box(L, W, H)
        
        # Mounting holes
        pts = [(-L/2 + 10, -W/2 + 90), (-L/2 + 90, -W/2 + 10)]
        block = block.faces(">Z").workplane().pushPoints(pts).hole(9.0)
        
        # Central counterbore
        block = block.faces(">Z").workplane().cboreHole(14.0, 20.0, 12.6)
        block = block.edges().chamfer(0.5)
        
        return block
    
    @staticmethod
    def create_stepped_shaft(params: Dict) -> cq.Workplane:
        """Create PART-03: Stepped Shaft"""
        D = params.get("diameter", 50.0)
        L = params.get("length", 50.0)
        sD = params.get("shoulder_diameter", 40.0)
        sL = params.get("shoulder_length", 20.0)
        
        large_cyl = cq.Workplane("XY").cylinder(sL, D/2).translate((0, 0, sL/2))
        small_len = L - sL
        small_cyl = cq.Workplane("XY").cylinder(small_len, sD/2).translate((0, 0, sL + small_len/2))
        
        shaft = large_cyl.union(small_cyl)
        shaft = shaft.edges().chamfer(0.5)
        
        return shaft
    
    @staticmethod
    def create_wheel(params: Dict) -> cq.Workplane:
        """Create PART-04: Wheel"""
        oD = params.get("outer_diameter", 250.0)
        W = params.get("width", 30.0)
        bD = params.get("bore_diameter", 40.0)
        
        disc = cq.Workplane("XY").cylinder(W, oD/2)
        disc = disc.faces(">Z").workplane().hole(bD)
        disc = disc.edges().chamfer(0.5)
        
        return disc
    
    @staticmethod
    def create_threaded_shaft(params: Dict) -> cq.Workplane:
        """Create PART-05: Threaded Shaft"""
        D = params.get("diameter", 20.0)
        L = params.get("length", 40.0)
        flange_dia = 30.0
        flange_thick = 5.0
        
        main_len = L - flange_thick
        main = cq.Workplane("XY").cylinder(main_len, D/2).translate((0, 0, main_len/2))
        flange = cq.Workplane("XY").cylinder(flange_thick, flange_dia/2).translate((0, 0, L - flange_thick/2))
        
        shaft = main.union(flange)
        shaft = shaft.faces(">Z").workplane().hole(6.8, 15.0)
        shaft = shaft.edges().chamfer(0.5)
        
        return shaft
    
    @staticmethod
    def create_slotted_plate(params: Dict) -> cq.Workplane:
        """Create PART-06: Slotted Plate"""
        L = params.get("length", 350.0)
        W = params.get("width", 50.0)
        H = params.get("height", 20.0)
        
        plate = cq.Workplane("XY").box(W, L, H)
        
        # Holes on the plate
        plate = plate.faces(">Z").workplane().center(0, -L/2 + 25.0).hole(20.0)
        plate = plate.faces(">Z").workplane().center(0, L/2 - 25.0).hole(25.0)
        plate = plate.edges().chamfer(0.5)
        
        return plate
    
    @staticmethod
    def create_side_block(params: Dict) -> cq.Workplane:
        """Create PART-07: Side Block"""
        L = params.get("length", 220.0)
        W = params.get("width", 135.0)
        H = params.get("height", 75.0)
        
        block = cq.Workplane("XZ").box(L, H, W)
        
        # Step cutout
        cut_w = 30.0
        cut_h = W - 115.0
        cut_box = cq.Workplane("XZ").box(L + 10, cut_h, cut_w).translate((0, W/2 - cut_w/2, W/2 - cut_h/2))
        block = block.cut(cut_box)
        
        # M8 holes
        pts = [(-L/2 + 10, -W/2 + 25.0), (L/2 - 10, -W/2 + 25.0)]
        block = block.faces("<Y").workplane().pushPoints(pts).hole(6.8, 33.8)
        block = block.edges().chamfer(0.5)
        
        return block
    
    @staticmethod
    def create_top_plate(params: Dict) -> cq.Workplane:
        """Create PART-08: Top Plate (trapezoidal)"""
        L = params.get("length", 140.0)
        W = params.get("width", 100.0)
        H = params.get("height", 20.0)
        
        # Trapezoidal profile
        pts = [
            (-W/2, -H/2),
            (W/2, -H/2),
            (W/2 - H, H/2),
            (-W/2, H/2)
        ]
        
        plate = cq.Workplane("XZ").polyline(pts).close().extrude(L/2, both=True)
        plate = plate.faces(">Z").workplane(origin=(0, 0, H/2)).center(-W/2 + 20.0, 0).hole(9.0)
        plate = plate.edges().chamfer(0.5)
        
        return plate
    
    @staticmethod
    def create_shaft_3(params: Dict) -> cq.Workplane:
        """Create PART-09: Shaft 3"""
        OD = params.get("outer_diameter", 25.0)
        L = params.get("length", 25.0)
        bore_dia = params.get("bore_diameter", 8.0)
        
        shaft = cq.Workplane("XY").cylinder(L, OD/2)
        shaft = shaft.faces(">Z").workplane().hole(bore_dia)
        shaft = shaft.edges().chamfer(0.5)
        
        return shaft


def generate_assembly_machine(output_file: str) -> None:
    """Generate and assemble all 9 components"""
    
    print("=" * 70)
    print("ASSEMBLY MACHINE GENERATOR (Docker Version)")
    print("=" * 70)
    
    builder = AssemblyMachineBuilder()
    registry = ComponentRegistry()
    
    print("\nGenerating components...")
    components = {}
    
    # Generate all parts
    components["base_plate"] = builder.create_base_plate(registry.PART_01_BASE_PLATE["params"])
    components["support_block_front"] = builder.create_support_block(registry.PART_02_SUPPORT_BLOCK["params"])
    components["support_block_back"] = builder.create_support_block(registry.PART_02_SUPPORT_BLOCK["params"])
    components["stepped_shaft"] = builder.create_stepped_shaft(registry.PART_03_STEPPED_SHAFT["params"])
    components["wheel"] = builder.create_wheel(registry.PART_04_WHEEL["params"])
    components["threaded_shaft"] = builder.create_threaded_shaft(registry.PART_05_THREADED_SHAFT["params"])
    components["slotted_plate"] = builder.create_slotted_plate(registry.PART_06_SLOTTED_PLATE["params"])
    components["side_block_left"] = builder.create_side_block(registry.PART_07_SIDE_BLOCK["params"])
    components["side_block_right"] = builder.create_side_block(registry.PART_07_SIDE_BLOCK["params"])
    components["top_plate"] = builder.create_top_plate(registry.PART_08_TOP_PLATE["params"])
    components["shaft_3"] = builder.create_shaft_3(registry.PART_09_SHAFT_3["params"])
    
    print("✓ All 9 components created")
    
    print("\nPositioning components...")
    positioned = {
        "base_plate": components["base_plate"].translate((0, 0, 0)),
        "support_block_front": components["support_block_front"].translate((-200, -100, 20)),
        "support_block_back": components["support_block_back"].translate((200, -100, 20)),
        "stepped_shaft": components["stepped_shaft"].translate((0, 150, 100)).rotateZ(90),
        "wheel": components["wheel"].translate((0, 150, 80)).rotateZ(90),
        "threaded_shaft": components["threaded_shaft"].translate((0, -150, 100)),
        "slotted_plate": components["slotted_plate"].translate((0, 0, 50)),
        "side_block_left": components["side_block_left"].translate((-200, -100, 100)),
        "side_block_right": components["side_block_right"].translate((200, -100, 100)),
        "top_plate": components["top_plate"].translate((0, 0, 180)),
        "shaft_3": components["shaft_3"].translate((0, 0, 130))
    }
    
    print("✓ Components positioned")
    
    print("\nAssembling...")
    assembly = positioned["base_plate"]
    for name in ["support_block_front", "support_block_back", "stepped_shaft", "wheel",
                 "threaded_shaft", "slotted_plate", "side_block_left", "side_block_right",
                 "top_plate", "shaft_3"]:
        assembly = assembly.union(positioned[name])
    
    print("✓ Assembly complete")
    
    print(f"\nExporting to {output_file}...")
    assembly.val().exportStep(output_file)
    
    print("\n" + "=" * 70)
    print("✓ ASSEMBLY GENERATION COMPLETE")
    print("=" * 70)
    print(f"Output file: {output_file}")
    print(f"File size: {os.path.getsize(output_file) / 1024:.2f} KB")


if __name__ == "__main__":
    output_file = sys.argv[1] if len(sys.argv) > 1 else "assembly_machine.step"
    
    try:
        generate_assembly_machine(output_file)
    except Exception as e:
        print(f"\n✗ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
