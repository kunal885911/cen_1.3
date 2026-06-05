from unittest.mock import patch
from components.base_component import BaseComponent
from cad.housing.generator import generate_housing_step_file

class HousingComponent(BaseComponent):
    """
    Wrapper for the existing Housing CAD generation logic.
    """
    component_type = "housing"

    def export_step(self, filepath: str, component_type: str = ""):
        super().export_step(filepath, component_type="housing")

    def generate(self):
        """
        Generate the CAD solid by wrapping the existing generation code.
        """
        with patch("cadquery.exporters.export") as mock_export:
            generate_housing_step_file(self.params, "dummy.step")
            self.solid = mock_export.call_args[0][0]
            
        return self.solid

    def get_connectors(self) -> dict:
        """
        Return connector definitions for the Housing.
        """
        length = self.params.get("length", 0.0)
        width = self.params.get("width", 0.0)
        height = self.params.get("height", 0.0)
        
        return {
            "top_face": {
                "position": (0, 0, height),
                "axis": (0, 0, 1),
                "type": "face",
                "diameter": None,
                "compatibility": ["face"]
            },
            "bottom_face": {
                "position": (0, 0, 0),
                "axis": (0, 0, -1),
                "type": "face",
                "diameter": None,
                "compatibility": ["face"]
            },
            "front_face": {
                "position": (0, -width / 2.0, height / 2.0),
                "axis": (0, -1, 0),
                "type": "face",
                "diameter": None,
                "compatibility": ["face"]
            },
            "back_face": {
                "position": (0, width / 2.0, height / 2.0),
                "axis": (0, 1, 0),
                "type": "face",
                "diameter": None,
                "compatibility": ["face"]
            },
            "left_face": {
                "position": (-length / 2.0, 0, height / 2.0),
                "axis": (-1, 0, 0),
                "type": "face",
                "diameter": None,
                "compatibility": ["face"]
            },
            "right_face": {
                "position": (length / 2.0, 0, height / 2.0),
                "axis": (1, 0, 0),
                "type": "face",
                "diameter": None,
                "compatibility": ["face"]
            }
        }
