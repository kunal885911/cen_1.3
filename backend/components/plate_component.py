from unittest.mock import patch
from components.base_component import BaseComponent
from cad.plate.generator import generate_plate_step_file

class PlateComponent(BaseComponent):
    """
    Wrapper for the existing Plate CAD generation logic.
    """
    component_type = "plate"

    def export_step(self, filepath: str, component_type: str = ""):
        super().export_step(filepath, component_type="plate")

    def generate(self):
        """
        Generate the CAD solid by wrapping the existing generation code.
        We intercept the cadquery.exporters.export call to capture the Workplane.
        """
        with patch("cadquery.exporters.export") as mock_export:
            generate_plate_step_file(self.params, "dummy.step")
            self.solid = mock_export.call_args[0][0]
            
        return self.solid

    def get_connectors(self) -> dict:
        """
        Return connector definitions for the plate.
        """
        length = self.params.get("length", 0.0)
        width = self.params.get("width", 0.0)
        thickness = max(6.0, 0.05 * width)
        
        return {
            "top_face": {
                "position": (0, 0, thickness / 2.0),
                "axis": (0, 0, 1),
                "type": "face",
                "diameter": None,
                "compatibility": ["face"]
            },
            "bottom_face": {
                "position": (0, 0, -thickness / 2.0),
                "axis": (0, 0, -1),
                "type": "face",
                "diameter": None,
                "compatibility": ["face"]
            },
            "front_face": {
                "position": (0, -width / 2.0, 0),
                "axis": (0, -1, 0),
                "type": "face",
                "diameter": None,
                "compatibility": ["face"]
            },
            "back_face": {
                "position": (0, width / 2.0, 0),
                "axis": (0, 1, 0),
                "type": "face",
                "diameter": None,
                "compatibility": ["face"]
            }
        }
