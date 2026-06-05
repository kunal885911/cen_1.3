import sys
import os
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.append(os.path.join(os.path.dirname(__file__), "backend"))

from components.shaft_component import ShaftComponent
from components.flange_component import FlangeComponent
from components.ubracket_component import UBracketComponent
from assembly.assembler import Assembler

parts = {
    "shaft1": ShaftComponent(diameter=20, length=100),
    "flange1": FlangeComponent(inner_diameter=22, thickness=15),
    "ubracket1": UBracketComponent(length=80, height=60, width=50, thickness=5)
}

connections = [
    ("shaft1.right_end", "flange1.back_center"),
    ("flange1.front_center", "ubracket1.base_face")
]

assembler = Assembler()
assembler.assemble(parts, connections)
for log in assembler.assembly_log:
    print(log)
