from unittest.mock import patch
from components.base_component import BaseComponent
from cad.flange.generator import generate_flange_step_file

class FlangeComponent(BaseComponent):
    """
    Wrapper for the existing Flange CAD generation logic.
    """
    component_type = "flange"

    def export_step(self, filepath: str, component_type: str = ""):
        super().export_step(filepath, component_type="flange")

    def generate(self):
        """
        Generate the CAD solid by wrapping the existing generation code.
        """
        with patch("cadquery.exporters.export") as mock_export:
            generate_flange_step_file(self.params, "dummy.step")
            self.solid = mock_export.call_args[0][0]
            
        return self.solid

    def get_connectors(self) -> dict:
        """
        Return connector definitions for the flange.
        """
        inner_diameter = self.params.get("inner_diameter", 0.0)
        thickness = 0.25 * inner_diameter
        hub_height = 1.2 * thickness
        
        return {
            "back_center": {
                "position": (0, 0, 0),
                "axis": (0, 0, -1),
                "type": "cylindrical",
                "diameter": inner_diameter,
                "compatibility": ["cylindrical", "hole"]
            },
            "front_center": {
                "position": (0, 0, hub_height),
                "axis": (0, 0, 1),
                "type": "cylindrical",
                "diameter": inner_diameter,
                "compatibility": ["cylindrical", "hole"]
            },
            "bolt_holes": {
                "position": (0, 0, thickness),
                "axis": (0, 0, 1),
                "type": "hole",
                "diameter": None,
                "compatibility": ["cylindrical", "hole"]
            }
        }
