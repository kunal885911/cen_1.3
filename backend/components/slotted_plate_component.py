import cadquery as cq
from components.base_component import BaseComponent

class SlottedPlateComponent(BaseComponent):
    component_type = "slotted_plate"

    def generate(self):
        L = self.params.get("length", 350.0)
        W = self.params.get("width", 50.0)
        H = self.params.get("height", 20.0)
        
        plate = cq.Workplane("XY").box(W, L, H)
        
        plate = plate.faces(">Z").workplane().center(0, -L/2 + 25.0).hole(20.0)
        plate = plate.faces(">Z").workplane().center(0, L/2 - 25.0).hole(25.0)
        plate = plate.edges().chamfer(0.5)
        
        self.solid = plate
        return self.solid

    def get_connectors(self) -> dict:
        L = self.params.get("length", 350.0)
        W = self.params.get("width", 50.0)
        H = self.params.get("height", 20.0)
        
        return {
            "front_face": {"position": (0, 0,  H/2), "axis": (0, 0,  1), "type": "face"},
            "back_face":  {"position": (0, 0, -H/2), "axis": (0, 0, -1), "type": "face"},
        }
