from unittest.mock import patch
from components.base_component import BaseComponent
from cad.brackets.ubracket_generator import generate_ubracket_step_file

class UBracketComponent(BaseComponent):
    """
    Wrapper for the existing UBracket CAD generation logic.
    """
    component_type = "ubracket"

    def export_step(self, filepath: str, component_type: str = ""):
        super().export_step(filepath, component_type="ubracket")

    def generate(self):
        """
        Generate the CAD solid by wrapping the existing generation code.
        """
        with patch("cadquery.exporters.export") as mock_export:
            generate_ubracket_step_file(self.params, "dummy.step")
            self.solid = mock_export.call_args[0][0]
            
        return self.solid

    def get_connectors(self) -> dict:
        """
        Return connector definitions for the U-Bracket.
        """
        length = self.params.get("length", 0.0)
        height = self.params.get("height", 0.0)
        width = self.params.get("width", 0.0)
        
        thickness = 0.1 * width
        
        return {
            "base_face": {
                "position": (0, 0, 0),
                "axis": (0, 0, -1),
                "type": "face",
                "diameter": None,
                "compatibility": ["face"]
            },
            "top_open": {
                "position": (0, 0, thickness + height),
                "axis": (0, 0, 1),
                "type": "face",
                "diameter": None,
                "compatibility": ["face"]
            },
            "left_wall": {
                "position": (0, -width / 2.0, thickness + height / 2.0),
                "axis": (0, -1, 0),
                "type": "face",
                "diameter": None,
                "compatibility": ["face"]
            },
            "right_wall": {
                "position": (0, width / 2.0, thickness + height / 2.0),
                "axis": (0, 1, 0),
                "type": "face",
                "diameter": None,
                "compatibility": ["face"]
            },
            "front_face": {
                "position": (length / 2.0, 0, thickness + height / 2.0),
                "axis": (1, 0, 0),
                "type": "face",
                "diameter": None,
                "compatibility": ["face"]
            }
        }
