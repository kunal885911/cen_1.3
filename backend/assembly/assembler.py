from pathlib import Path

from assembly.mating import ConnectorMatcher
from assembly.transformations import compute_mate_transform, apply_transform, apply_transform_to_connector

class Assembler:
    def __init__(self):
        self.parts: dict = {}          # id → component instance
        self.positioned: dict = {}     # id → transformed solid
        self.current_connectors: dict = {} # id → dict of connector definitions
        self.matcher = ConnectorMatcher()

    def assemble(self, parts: dict, connections: list) -> "Assembler":
        """
        parts: {"shaft1": ShaftComponent, "flange1": FlangeComponent, ...}
        connections: [("shaft1.right_end", "flange1.center"), ...]
        """
        self.parts = parts
        self.assembly_log = []

        # Step 1: generate all solids
        for part_id, part in parts.items():
            part.generate()

        # Step 2: live_connectors tracks WORLD-SPACE connector positions.
        live_connectors = {}
        for part_id, part in parts.items():
            live_connectors[part_id] = {
                name: dict(conn)
                for name, conn in part.get_connectors().items()
            }

        # Step 3: copy solids into positioned dict (first part stays at origin)
        self.positioned = {}
        for part_id, part in parts.items():
            self.positioned[part_id] = part.solid

        placed = set()
        first_id = next(iter(parts))
        placed.add(first_id)

        # Step 4: process each connection in order
        for conn_str_a, conn_str_b in connections:
            part_a_id, conn_a_name = conn_str_a.split(".", 1)
            part_b_id, conn_b_name = conn_str_b.split(".", 1)

            if part_a_id not in parts:
                raise ValueError(f"Part '{part_a_id}' not found in assembly.")
            if part_b_id not in parts:
                raise ValueError(f"Part '{part_b_id}' not found in assembly.")

            if conn_a_name not in live_connectors[part_a_id]:
                available = list(live_connectors[part_a_id].keys())
                raise ValueError(
                    f"Connector '{conn_a_name}' not found on '{part_a_id}'. Available: {available}"
                )
            if conn_b_name not in live_connectors[part_b_id]:
                available = list(live_connectors[part_b_id].keys())
                raise ValueError(
                    f"Connector '{conn_b_name}' not found on '{part_b_id}'. Available: {available}"
                )

            # Ensure Part A is placed. If not, we could swap them, 
            # but user instruction assumes part_a is target and part_b is source.
            if part_a_id not in placed and part_b_id in placed:
                part_a_id, part_b_id = part_b_id, part_a_id
                conn_a_name, conn_b_name = conn_b_name, conn_a_name

            conn_a = live_connectors[part_a_id][conn_a_name]  # target (fixed)
            conn_b = live_connectors[part_b_id][conn_b_name]  # source (moves)

            from assembly.transformations import compute_mate_transform, apply_transform, apply_transform_to_connector
            transform = compute_mate_transform(conn_b, conn_a)

            self.positioned[part_b_id] = apply_transform(
                self.positioned[part_b_id], transform
            )

            for name in live_connectors[part_b_id]:
                live_connectors[part_b_id][name] = apply_transform_to_connector(
                    live_connectors[part_b_id][name], transform
                )

            # BUG 4 logging
            import numpy as np
            new_conn_b_pos = np.array(live_connectors[part_b_id][conn_b_name]["position"])
            target_pos     = np.array(conn_a["position"])
            gap = float(np.linalg.norm(new_conn_b_pos - target_pos))

            self.assembly_log.append(
                f"[OK] {conn_str_a} ↔ {conn_str_b} | gap={gap:.6f}mm "
                f"| rotation={transform['rotation_angle_deg']:.2f}deg "
                f"| translation={transform['translation']}"
            )
            if gap > 0.001:
                self.assembly_log.append(
                    f"[WARN] Gap {gap:.4f}mm detected — connector positions may be wrong"
                )

            placed.add(part_b_id)

        self.live_connectors = live_connectors
        return self

    def export_step(self, output_dir: str):
        """
        Always produces all 3 outputs — no mode flag needed.
        """
        import cadquery as cq
        import os
        from components.color_registry import get_color
        out_dir = Path(output_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        
        # OUTPUT 1 — assembly_colored.step
        master_assy = cq.Assembly(name="full_assembly")
        for part_id, solid in self.positioned.items():
            component_type = self.parts[part_id].component_type
            color_data = get_color(component_type)
            color = cq.Color(color_data["r"], color_data["g"], color_data["b"])
            master_assy.add(solid, name=part_id, color=color)
        master_assy.save(os.path.join(output_dir, "assembly_colored.step"))

        # OUTPUT 2 — individual/{part_id}.step
        os.makedirs(os.path.join(output_dir, "individual"), exist_ok=True)
        for part_id, solid in self.positioned.items():
            component_type = self.parts[part_id].component_type
            color_data = get_color(component_type)
            color = cq.Color(color_data["r"], color_data["g"], color_data["b"])
            part_assy = cq.Assembly(name=f"{part_id}_assy")
            part_assy.add(solid, name=part_id, color=color)
            part_assy.save(os.path.join(output_dir, "individual", f"{part_id}.step"))

        # OUTPUT 3 — assembly_fused.step
        if self.positioned:
            first_id = list(self.positioned.keys())[0]
            fused = self.positioned[first_id]
            for part_id, solid in list(self.positioned.items())[1:]:
                try:
                    fused = fused.union(solid)
                except Exception:
                    pass  # skip if boolean fails (non-manifold edge case)
            single_assy = cq.Assembly(name="fused_assy")
            single_assy.add(fused, name="fused_body")
            single_assy.save(os.path.join(output_dir, "assembly_fused.step"))

