import cadquery as cq
from components.base_component import BaseComponent

class SteppedShaftComponent(BaseComponent):
    component_type = "stepped_shaft"

    def generate(self):
        D = self.params.get("diameter", 50.0)
        L = self.params.get("length", 50.0)
        sD = self.params.get("shoulder_diameter", 40.0)
        sL = self.params.get("shoulder_length", 20.0)
        
        large_cyl = cq.Workplane("XY").cylinder(sL, D/2).translate((0, 0, sL/2))
        small_len = L - sL
        small_cyl = cq.Workplane("XY").cylinder(small_len, sD/2).translate((0, 0, sL + small_len/2))
        
        shaft = large_cyl.union(small_cyl)
        shaft = shaft.edges().chamfer(0.5)
        
        self.solid = shaft
        return self.solid

    def get_connectors(self) -> dict:
        D = self.params.get("diameter", 50.0)
        L = self.params.get("length", 50.0)
        
        return {
            "left_end": {"position": (0, 0, 0), "axis": (0, 0, -1), "type": "face"},
            "right_end": {"position": (0, 0, L), "axis": (0, 0, 1), "type": "face"},
        }
