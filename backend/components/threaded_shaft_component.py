import cadquery as cq
from components.base_component import BaseComponent

class ThreadedShaftComponent(BaseComponent):
    component_type = "threaded_shaft"

    def generate(self):
        D = self.params.get("diameter", 20.0)
        L = self.params.get("length", 40.0)
        flange_dia = 30.0
        flange_thick = 5.0
        
        main_len = L - flange_thick
        main = cq.Workplane("XY").cylinder(main_len, D/2).translate((0, 0, main_len/2))
        flange = cq.Workplane("XY").cylinder(flange_thick, flange_dia/2).translate((0, 0, L - flange_thick/2))
        
        shaft = main.union(flange)
        shaft = shaft.faces(">Z").workplane().hole(6.8, 15.0)
        shaft = shaft.edges().chamfer(0.5)
        
        self.solid = shaft
        return self.solid

    def get_connectors(self) -> dict:
        D = self.params.get("diameter", 20.0)
        L = self.params.get("length", 40.0)
        
        return {
            "left_end": {"position": (0, 0, 0), "axis": (0, 0, -1), "type": "face"},
            "right_end": {"position": (0, 0, L), "axis": (0, 0, 1), "type": "face"},
        }
