from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class AssemblyMachineSchema:
    """
    Schema for the Assembly Machine (9-part complex geometry)
    
    Parts:
    1. Base Plate (PART-01)
    2. Support Block x2 (PART-02)
    3. Stepped Shaft (PART-03)
    4. Wheel (PART-04)
    5. Threaded Shaft (PART-05)
    6. Slotted Plate (PART-06)
    7. Side Block x2 (PART-07)
    8. Top Plate (PART-08)
    9. Shaft 3 / Cylindrical Spacer (PART-09)
    """
    
    # Base Plate Configuration (PART-01)
    base_plate_length: float = 500.0
    base_plate_width: float = 300.0
    base_plate_height: float = 20.0
    base_plate_hole_diameter: float = 9.0
    
    # Support Block Configuration (PART-02) x2
    support_block_length: float = 100.0
    support_block_width: float = 100.0
    support_block_height: float = 80.0
    support_block_bore_diameter: float = 14.0
    support_block_slot_width: float = 12.6
    
    # Stepped Shaft Configuration (PART-03)
    stepped_shaft_diameter: float = 50.0
    stepped_shaft_length: float = 50.0
    stepped_shaft_shoulder_diameter: float = 40.0
    stepped_shaft_shoulder_length: float = 20.0
    stepped_shaft_keyway_width: float = 10.0
    
    # Wheel Configuration (PART-04)
    wheel_outer_diameter: float = 250.0
    wheel_width: float = 30.0
    wheel_bore_diameter: float = 40.0
    wheel_keyway_width: float = 10.0
    wheel_m8_distance: float = 100.0
    
    # Threaded Shaft Configuration (PART-05)
    threaded_shaft_diameter: float = 20.0
    threaded_shaft_length: float = 40.0
    threaded_shaft_thread_length: float = 13.8
    
    # Slotted Plate Configuration (PART-06)
    slotted_plate_length: float = 350.0
    slotted_plate_width: float = 50.0
    slotted_plate_height: float = 20.0
    slotted_plate_bottom_hole_dia: float = 20.0
    slotted_plate_top_hole_dia: float = 25.0
    
    # Side Block Configuration (PART-07) x2
    side_block_length: float = 220.0
    side_block_width: float = 135.0
    side_block_depth: float = 75.0
    side_block_bore_diameter: float = 33.8
    
    # Top Plate Configuration (PART-08)
    top_plate_length: float = 140.0
    top_plate_width: float = 100.0
    top_plate_height: float = 20.0
    top_plate_hole_diameter: float = 9.0
    
    # Shaft 3 Configuration (PART-09)
    shaft_3_outer_diameter: float = 25.0
    shaft_3_length: float = 25.0
    shaft_3_bore_diameter: float = 8.0
    
    # Assembly positioning
    base_position: tuple = (0, 0, 0)
    
    # Support block positions (front and back on base plate)
    support_block_front_position: tuple = (-200, -100, 20)  # Left-front
    support_block_back_position: tuple = (200, -100, 20)    # Right-front
    
    # Side block positions (left and right)
    side_block_left_position: tuple = (-200, -100, 100)
    side_block_right_position: tuple = (200, -100, 100)
    
    # Top plate position
    top_plate_position: tuple = (0, 0, 180)
    
    # Stepped shaft position (central axis)
    stepped_shaft_position: tuple = (0, 150, 100)
    
    # Wheel position (on stepped shaft)
    wheel_position: tuple = (0, 150, 80)
    
    # Threaded shaft position (secondary axis)
    threaded_shaft_position: tuple = (0, -150, 100)
    
    # Slotted plate position (vertical connector)
    slotted_plate_position: tuple = (0, 0, 50)
    
    # Shaft 3 position (spacer)
    shaft_3_position: tuple = (0, 0, 130)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert schema to dictionary for JSON serialization"""
        return {
            "base_plate": {
                "length": self.base_plate_length,
                "width": self.base_plate_width,
                "height": self.base_plate_height,
                "hole_diameter": self.base_plate_hole_diameter
            },
            "support_block": {
                "length": self.support_block_length,
                "width": self.support_block_width,
                "height": self.support_block_height,
                "bore_diameter": self.support_block_bore_diameter
            },
            "stepped_shaft": {
                "diameter": self.stepped_shaft_diameter,
                "length": self.stepped_shaft_length,
                "shoulder_diameter": self.stepped_shaft_shoulder_diameter
            },
            "wheel": {
                "outer_diameter": self.wheel_outer_diameter,
                "width": self.wheel_width,
                "bore_diameter": self.wheel_bore_diameter
            },
            "threaded_shaft": {
                "diameter": self.threaded_shaft_diameter,
                "length": self.threaded_shaft_length
            },
            "slotted_plate": {
                "length": self.slotted_plate_length,
                "width": self.slotted_plate_width,
                "height": self.slotted_plate_height
            },
            "side_block": {
                "length": self.side_block_length,
                "width": self.side_block_width,
                "depth": self.side_block_depth
            },
            "top_plate": {
                "length": self.top_plate_length,
                "width": self.top_plate_width,
                "height": self.top_plate_height
            },
            "shaft_3": {
                "outer_diameter": self.shaft_3_outer_diameter,
                "length": self.shaft_3_length,
                "bore_diameter": self.shaft_3_bore_diameter
            }
        }
