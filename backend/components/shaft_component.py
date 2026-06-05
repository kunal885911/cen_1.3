from unittest.mock import patch
from components.base_component import BaseComponent
from cad.shaft.generator import generate_shaft_step_file

class ShaftComponent(BaseComponent):
    """
    Wrapper for the existing Shaft CAD generation logic.
    """
    component_type = "shaft"
    
    def export_step(self, filepath: str, component_type: str = ""):
        super().export_step(filepath, component_type="shaft")

    def generate(self):
        """
        Generate the CAD solid by wrapping the existing generation code.
        We use unittest.mock.patch to intercept the cadquery.exporters.export
        call inside the generator so we can capture the solid object without
        modifying the existing geometry logic.
        """
        # Call existing generation code with our params.
        # It normally exports a STEP file directly. We intercept the export.
        with patch("cadquery.exporters.export") as mock_export:
            # The original code expects a params dictionary and a step_path.
            generate_shaft_step_file(self.params, "dummy.step")
            
            # The export function is called with (solid, path, format)
            # We extract the solid from the first argument of the mock call.
            self.solid = mock_export.call_args[0][0]
            
        return self.solid

    def get_connectors(self) -> dict:
        """
        Return connector definitions for the shaft.
        """
        diameter = self.params.get("diameter", 0.0)
        length = self.params.get("length", 0.0)
        
        return {
            "left_end": {
                "position": (0, 0, 0),
                "axis": (0, 0, -1),
                "type": "cylindrical",
                "diameter": diameter,
                "compatibility": ["cylindrical", "hole"]
            },
            "right_end": {
                "position": (0, 0, length),
                "axis": (0, 0, 1),
                "type": "cylindrical",
                "diameter": diameter,
                "compatibility": ["cylindrical", "hole"]
            }
        }
