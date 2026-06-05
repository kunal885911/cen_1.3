import cadquery as cq
from components.base_component import BaseComponent

class Shaft3Component(BaseComponent):
    component_type = "shaft_3"

    def generate(self):
        # Part-09: SHAFT 3 (Cylindrical Spacer)
        # From drawing CEN-26-XXX-PART-09
        
        OD = self.params.get("outer_diameter", 25.0)
        L = self.params.get("length", 25.0)
        bore_dia = self.params.get("bore_diameter", 8.0)  # M8 bore
        
        # Cylindrical spacer on XY plane, length along Z
        shaft = cq.Workplane("XY").cylinder(L, OD/2)
        
        # Central M8 bore (8.0mm diameter) - can be plain or tapped
        shaft = shaft.faces(">Z").workplane().hole(bore_dia)
        
        # Chamfer all edges
        shaft = shaft.edges().chamfer(0.5)
        
        self.solid = shaft
        return self.solid

    def get_connectors(self) -> dict:
        OD = self.params.get("outer_diameter", 25.0)
        L = self.params.get("length", 25.0)
        bore_dia = self.params.get("bore_diameter", 8.0)
        
        return {
            "top_face":      {"position": (0, 0,  L/2), "axis": (0, 0,  1), "type": "face"},
            "bottom_face":   {"position": (0, 0, -L/2), "axis": (0, 0, -1), "type": "face"},
            "cylindrical_face": {"position": (0, 0, 0), "axis": (1, 0, 0), "type": "cylindrical", "diameter": OD},
            "bore_top":      {"position": (0, 0,  L/2), "axis": (0, 0,  1), "type": "hole", "diameter": bore_dia},
            "bore_bottom":   {"position": (0, 0, -L/2), "axis": (0, 0, -1), "type": "hole", "diameter": bore_dia}
        }
