from unittest.mock import patch
from components.base_component import BaseComponent
from cad.brackets.lbracket_generator import generate_lbracket_step_file

class LBracketComponent(BaseComponent):
    """
    Wrapper for the existing LBracket CAD generation logic.
    """
    component_type = "lbracket"

    def export_step(self, filepath: str, component_type: str = ""):
        super().export_step(filepath, component_type="lbracket")

    def generate(self):
        """
        Generate the CAD solid by wrapping the existing generation code.
        """
        with patch("cadquery.exporters.export") as mock_export:
            generate_lbracket_step_file(self.params, "dummy.step")
            self.solid = mock_export.call_args[0][0]
            
        return self.solid

    def get_connectors(self) -> dict:
        """
        Return connector definitions for the L-Bracket.
        """
        length_1 = self.params.get("length_1", 0.0)
        length_2 = self.params.get("length_2", 0.0)
        width = self.params.get("width", 0.0)
        
        thickness = 0.1 * width
        
        return {
            "face_1": {
                "position": (length_1, thickness / 2.0, thickness / 2.0),
                "axis": (1, 0, 0),
                "type": "face",
                "diameter": None,
                "compatibility": ["face"]
            },
            "face_2": {
                "position": (thickness / 2.0, length_2, thickness / 2.0),
                "axis": (0, 1, 0),
                "type": "face",
                "diameter": None,
                "compatibility": ["face"]
            },
            "back_face_1": {
                "position": (length_1 / 2.0, 0, thickness / 2.0),
                "axis": (0, -1, 0),
                "type": "face",
                "diameter": None,
                "compatibility": ["face"]
            },
            "back_face_2": {
                "position": (0, length_2 / 2.0, thickness / 2.0),
                "axis": (-1, 0, 0),
                "type": "face",
                "diameter": None,
                "compatibility": ["face"]
            }
        }
