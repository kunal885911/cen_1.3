import cadquery as cq
from components.base_component import BaseComponent

class BasePlateComponent(BaseComponent):
    component_type = "base_plate"

    def generate(self):
        L = self.params.get("length", 500.0)
        W = self.params.get("width", 300.0)
        H = self.params.get("height", 20.0)
        hole_dia = self.params.get("hole_diameter", 9.0)
        
        # Base box on XY plane, thickness along Z
        plate = cq.Workplane("XY").box(L, W, H)
        
        # Holes on >Z face
        xs = [-L/2 + 40, -L/2 + 220, -L/2 + 410]
        ys = [-W/2 + 85, -W/2 + 215]
        pts = [(x, y) for x in xs for y in ys]
        
        plate = plate.faces(">Z").workplane().pushPoints(pts).hole(hole_dia)
        plate = plate.edges().chamfer(0.5)
        
        self.solid = plate
        return self.solid

    def get_connectors(self) -> dict:
        L = self.params.get("length", 500.0)
        W = self.params.get("width", 300.0)
        H = self.params.get("height", 20.0)
        
        return {
            "top_face":    {"position": (0, 0,  H/2), "axis": (0, 0,  1), "type": "face"},
            "bottom_face": {"position": (0, 0, -H/2), "axis": (0, 0, -1), "type": "face"},
        }
