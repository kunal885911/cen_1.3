import cadquery as cq
from components.base_component import BaseComponent

class SideBlockComponent(BaseComponent):
    component_type = "side_block"

    def generate(self):
        L = self.params.get("length", 220.0)
        H = self.params.get("width", 135.0)
        W = self.params.get("top_cutout_width", 75.0)
        H_step = self.params.get("height", 115.0)
        
        block = cq.Workplane("XZ").box(L, W, H)
        
        cut_w = 30.0
        cut_h = H - H_step
        cut_box = cq.Workplane("XZ").box(L + 10, cut_w, cut_h).translate((0, W/2 - cut_w/2, H/2 - cut_h/2))
        block = block.cut(cut_box)
        
        pts = [(-L/2 + 10, -W/2 + 25.0), (L/2 - 10, -W/2 + 25.0)]
        block = block.faces("<Y").workplane().pushPoints(pts).hole(6.8, 33.8)
        block = block.edges().chamfer(0.5)
        
        self.solid = block
        return self.solid

    def get_connectors(self) -> dict:
        L = self.params.get("length", 220.0)
        H = self.params.get("width", 135.0)
        
        return {
            "left_face": {"position": (-L/2, 0, 0), "axis": (-1, 0, 0), "type": "face"},
            "right_face": {"position": (L/2, 0, 0), "axis": (1, 0, 0), "type": "face"},
        }
