import math

# Pre-defined valid mating pairs for the existing 7 models:
# shaft.right_end      ↔ flange.back_center
# shaft.left_end       ↔ flange.back_center
# flange.bolt_holes    ↔ lbracket.face_1
# lbracket.face_2      ↔ plate.top_face
# housing.bottom_face  ↔ plate.top_face
# ubracket.base_face   ↔ plate.top_face

MATING_RULES = {
    ("cylindrical", "cylindrical"): True,
    ("cylindrical", "hole"):        True,
    ("hole",        "cylindrical"): True,
    ("face",        "face"):        True,
    ("hole",        "face"):        True,
    ("face",        "hole"):        True,
    ("cylindrical", "face"):        True,
    ("face",        "cylindrical"): True,
}

class ConnectorMatcher:
    def check_compatibility(self, conn_a: dict, conn_b: dict) -> bool:
        """Return True if connector types are compatible per MATING_RULES."""
        # To add a new mating rule in the future, simply add the type tuple to MATING_RULES.
        type_a = conn_a.get("type")
        type_b = conn_b.get("type")
        return MATING_RULES.get((type_a, type_b), False)

    def validate_axis_alignment(
        self, conn_a: dict, conn_b: dict, tolerance_deg: float = 5.0
    ) -> bool:
        """
        Check that conn_a axis and conn_b axis are anti-parallel
        (within tolerance_deg degrees). Anti-parallel because mating
        faces point toward each other.
        Uses dot product: aligned if dot(a, -b) >= cos(tolerance_deg).
        
        Detailed Explanation:
        - When two components mate, their connecting faces should be touching, meaning 
          their normal vectors (axes) must point in exactly opposite directions.
        - Therefore, we want `conn_b`'s axis to be as close to `-conn_a`'s axis as possible.
        - The mathematical definition of the dot product between two unit vectors U and V 
          is U·V = cos(theta), where theta is the angle between them.
        - By calculating the dot product of conn_a.axis and -conn_b.axis, we get the cosine 
          of the angle between the aligned states.
        - If the dot product is greater than or equal to cos(tolerance_deg), it means the 
          angle is less than or equal to the tolerance.
        """
        a = conn_a.get("axis", (0, 0, 1))
        b = conn_b.get("axis", (0, 0, 1))
        
        # Calculate dot product of 'a' and '-b'
        # dot(a, -b) = a_x*(-b_x) + a_y*(-b_y) + a_z*(-b_z)
        dot_product = -(a[0]*b[0] + a[1]*b[1] + a[2]*b[2])
        
        # Normalize in case axes are not pure unit vectors
        mag_a = math.sqrt(a[0]**2 + a[1]**2 + a[2]**2)
        mag_b = math.sqrt(b[0]**2 + b[1]**2 + b[2]**2)
        
        if mag_a == 0 or mag_b == 0:
            return False
            
        normalized_dot = dot_product / (mag_a * mag_b)
        # Clamp to [-1, 1] to avoid floating point errors before trig functions
        normalized_dot = max(-1.0, min(1.0, normalized_dot))
        
        cos_tol = math.cos(math.radians(tolerance_deg))
        return normalized_dot >= cos_tol

    def get_mating_transform(self, conn_a: dict, conn_b: dict) -> dict:
        """
        Compute the translation and rotation needed to move the component
        owning conn_b so that conn_b aligns with conn_a.
        Returns:
        {
          "translation": (tx, ty, tz),
          "rotation_axis": (rx, ry, rz),
          "rotation_angle_deg": float
        }
        
        Detailed Explanation:
        - Translation: Computed directly as the vector from conn_b.position to conn_a.position.
          Moving part B by this translation puts conn_b exactly on top of conn_a.
        - Rotation: We need conn_b.axis to become -conn_a.axis.
          To find the rotation needed to rotate vector V1 to vector V2:
          1. The rotation axis is the cross product of V1 and V2, which gives a vector 
             perpendicular to both.
          2. The angle is the arccosine of the dot product of V1 and V2 (assuming unit vectors).
        """
        pos_a = conn_a.get("position", (0, 0, 0))
        pos_b = conn_b.get("position", (0, 0, 0))
        
        # Translation vector = Destination - Source
        tx = pos_a[0] - pos_b[0]
        ty = pos_a[1] - pos_b[1]
        tz = pos_a[2] - pos_b[2]
        
        axis_a = conn_a.get("axis", (0, 0, 1))
        axis_b = conn_b.get("axis", (0, 0, 1))
        
        mag_a = math.sqrt(sum(c**2 for c in axis_a))
        mag_b = math.sqrt(sum(c**2 for c in axis_b))
        
        # Normalized axes
        na = tuple(c/mag_a for c in axis_a)
        nb = tuple(c/mag_b for c in axis_b)
        
        # We want to rotate nb to align with -na (because mating faces point opposite ways)
        target = (-na[0], -na[1], -na[2])
        
        # Cross product: nb x target
        rx = nb[1]*target[2] - nb[2]*target[1]
        ry = nb[2]*target[0] - nb[0]*target[2]
        rz = nb[0]*target[1] - nb[1]*target[0]
        
        mag_cross = math.sqrt(rx**2 + ry**2 + rz**2)
        
        # Dot product for angle: nb . target
        dot_ab = nb[0]*target[0] + nb[1]*target[1] + nb[2]*target[2]
        dot_ab = max(-1.0, min(1.0, dot_ab))
        angle_rad = math.acos(dot_ab)
        angle_deg = math.degrees(angle_rad)
        
        # Handle parallel and anti-parallel cases
        if mag_cross < 1e-6:
            if dot_ab > 0:
                # Already perfectly aligned (nb == target)
                rotation_axis = (1.0, 0.0, 0.0)
                angle_deg = 0.0
            else:
                # Exactly opposite (nb == -target). Needs 180 deg flip around an arbitrary orthogonal axis.
                # If nb is mostly X, use Y axis, otherwise use X axis as a basis to find orthogonal.
                temp_axis = (1.0, 0.0, 0.0) if abs(nb[0]) < 0.9 else (0.0, 1.0, 0.0)
                # Cross product nb with temp_axis guarantees an orthogonal vector
                rx2 = nb[1]*temp_axis[2] - nb[2]*temp_axis[1]
                ry2 = nb[2]*temp_axis[0] - nb[0]*temp_axis[2]
                rz2 = nb[0]*temp_axis[1] - nb[1]*temp_axis[0]
                mag_cross2 = math.sqrt(rx2**2 + ry2**2 + rz2**2)
                rotation_axis = (rx2/mag_cross2, ry2/mag_cross2, rz2/mag_cross2)
                angle_deg = 180.0
        else:
            # Normal case
            rotation_axis = (rx/mag_cross, ry/mag_cross, rz/mag_cross)
            
        return {
            "translation": (tx, ty, tz),
            "rotation_axis": rotation_axis,
            "rotation_angle_deg": angle_deg
        }

    def validate_mate(
        self, part_a_id: str, conn_a_name: str,
        part_b_id: str, conn_b_name: str,
        components: dict
    ) -> dict:
        """
        Full validation report for a single connection.
        Raises ValueError with a clear message on failure.
        Returns a report dict on success:
        {
          "valid": True,
          "pair": "partA.connA ↔ partB.connB",
          "type_match": True,
          "axis_aligned": True,
          "transform": {...}
        }
        """
        if part_a_id not in components:
            raise ValueError(f"Part A '{part_a_id}' not found in components dictionary.")
        if part_b_id not in components:
            raise ValueError(f"Part B '{part_b_id}' not found in components dictionary.")
            
        part_a = components[part_a_id]
        part_b = components[part_b_id]
        
        conns_a = part_a.get_connectors()
        conns_b = part_b.get_connectors()
        
        if conn_a_name not in conns_a:
            raise ValueError(f"Connector '{conn_a_name}' not found on '{part_a_id}'.")
        if conn_b_name not in conns_b:
            raise ValueError(f"Connector '{conn_b_name}' not found on '{part_b_id}'.")
            
        conn_a = conns_a[conn_a_name]
        conn_b = conns_b[conn_b_name]
        
        if not self.check_compatibility(conn_a, conn_b):
            raise ValueError(f"Incompatible types: '{conn_a.get('type')}' cannot mate with '{conn_b.get('type')}'.")
            
        axis_aligned = self.validate_axis_alignment(conn_a, conn_b)
        transform = self.get_mating_transform(conn_a, conn_b)
        
        return {
            "valid": True,
            "pair": f"{part_a_id}.{conn_a_name} ↔ {part_b_id}.{conn_b_name}",
            "type_match": True,
            "axis_aligned": axis_aligned,
            "transform": transform
        }
