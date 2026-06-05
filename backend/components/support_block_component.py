import cadquery as cq
from components.base_component import BaseComponent

class SupportBlockComponent(BaseComponent):
    component_type = "support_block"

    def generate(self):
        L = self.params.get("length", 100.0)
        W = self.params.get("width", 100.0)
        H = self.params.get("height", 80.0)
        
        block = cq.Workplane("XY").box(L, W, H)
        
        pts = [(-L/2 + 10, -W/2 + 90), (-L/2 + 90, -W/2 + 10)]
        block = block.faces(">Z").workplane().pushPoints(pts).hole(9.0)
        
        block = block.faces(">Z").workplane().cboreHole(14.0, 20.0, 12.6)
        block = block.edges().chamfer(0.5)
        
        self.solid = block
        return self.solid

    def get_connectors(self) -> dict:
        L = self.params.get("length", 100.0)
        W = self.params.get("width", 100.0)
        H = self.params.get("height", 80.0)
        
        return {
            "top_face": {"position": (0, 0, H/2), "axis": (0, 0, 1), "type": "face"},
        }
