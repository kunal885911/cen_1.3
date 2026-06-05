import cadquery as cq
from components.base_component import BaseComponent

class TopPlateComponent(BaseComponent):
    component_type = "top_plate"

    def generate(self):
        L = self.params.get("length", 140.0)
        W = self.params.get("width", 100.0)
        H = self.params.get("height", 20.0)
        
        pts = [
            (-W/2, -H/2),
            (W/2, -H/2),
            (W/2 - H, H/2),
            (-W/2, H/2)
        ]
        
        plate = cq.Workplane("XZ").polyline(pts).close().extrude(L/2, both=True)
        plate = plate.faces(">Z").workplane(origin=(0, 0, H/2)).center(-W/2 + 20.0, 0).hole(9.0)
        plate = plate.edges().chamfer(0.5)
        
        self.solid = plate
        return self.solid

    def get_connectors(self) -> dict:
        L = self.params.get("length", 140.0)
        W = self.params.get("width", 100.0)
        H = self.params.get("height", 20.0)
        
        return {
            "top_face": {"position": (0, 0, H/2), "axis": (0, 0, 1), "type": "face"},
            "bottom_face": {"position": (0, 0, -H/2), "axis": (0, 0, -1), "type": "face"},
        }
