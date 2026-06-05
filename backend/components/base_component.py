import os

class BaseComponent:
    component_type: str = "unknown"

    def __init__(self, **params):
        self.params = params
        self.solid = None

    def generate(self):
        """Generate and return the CadQuery solid. Must set self.solid."""
        raise NotImplementedError

    def get_connectors(self) -> dict:
        """Return connector definitions for assembly mating.
        Format:
        {
          "connector_name": {
            "position": (x, y, z),   # world-space point
            "axis": (dx, dy, dz),     # normalized direction vector
            "type": str,              # "cylindrical", "face", "hole"
            "diameter": float|None,   # relevant for cylindrical/hole
            "compatibility": [str]    # list of compatible connector types
          }
        }
        """
        raise NotImplementedError

    def export_step(self, filepath: str, component_type: str = ""):
        """
        Export self.solid as a colored STEP file.
        """
        if self.solid is None:
            raise RuntimeError("Call generate() before export_step()")
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
        
        import cadquery as cq
        from .color_registry import get_color

        c_type = component_type if component_type else self.component_type
        color_data = get_color(c_type)
        color = cq.Color(color_data["r"], color_data["g"], color_data["b"])

        assy = cq.Assembly()
        assy.add(
            self.solid,
            name=c_type,
            color=color
        )
        assy.save(filepath)
