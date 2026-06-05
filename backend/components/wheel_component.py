import cadquery as cq
from components.base_component import BaseComponent

class WheelComponent(BaseComponent):
    component_type = "wheel"

    def generate(self):
        oD = self.params.get("outer_diameter", 250.0)
        W = self.params.get("width", 30.0)
        bD = self.params.get("bore_diameter", 40.0)
        
        disc = cq.Workplane("XY").cylinder(W, oD/2)
        disc = disc.faces(">Z").workplane().hole(bD)
        disc = disc.edges().chamfer(0.5)
        
        self.solid = disc
        return self.solid

    def get_connectors(self) -> dict:
        W = self.params.get("width", 30.0)
        bD = self.params.get("bore_diameter", 40.0)
        
        return {
            "front_face": {"position": (0, 0,  W/2), "axis": (0, 0,  1), "type": "face"},
            "back_face":  {"position": (0, 0, -W/2), "axis": (0, 0, -1), "type": "face"},
        }
