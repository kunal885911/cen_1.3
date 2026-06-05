import numpy as np

def normalize(v):
    v = np.array(v, dtype=float)
    n = np.linalg.norm(v)
    return v / n if n > 1e-10 else v

def rotate_vector(v, axis, angle_deg):
    """Rodrigues rotation formula — rotates vector v around axis by angle_deg."""
    v    = np.array(v, dtype=float)
    axis = normalize(np.array(axis, dtype=float))
    rad  = np.radians(angle_deg)
    return (v * np.cos(rad)
            + np.cross(axis, v) * np.sin(rad)
            + axis * np.dot(axis, v) * (1 - np.cos(rad)))

def compute_mate_transform(source_conn: dict, target_conn: dict) -> dict:
    """
    Computes transform to move the part owning source_conn
    so that source_conn aligns flush with target_conn.
    """
    # STEP 1 — ROTATION:
    source_dir = normalize(source_conn["axis"])
    target_dir = -normalize(target_conn["axis"])  # flip target axis

    cross = np.cross(source_dir, target_dir)
    cross_len = np.linalg.norm(cross)

    if cross_len < 1e-6:
        # axes already aligned or 180° apart
        dot = np.dot(source_dir, target_dir)
        if dot > 0:
            rotation_axis = (0, 0, 1)  # identity, no rotation needed
            angle = 0.0
        else:
            # exactly 180° — pick any perpendicular axis
            perp = np.cross(source_dir, [1,0,0])
            if np.linalg.norm(perp) < 1e-6:
                perp = np.cross(source_dir, [0,1,0])
            rotation_axis = tuple(normalize(perp))
            angle = 180.0
    else:
        rotation_axis = tuple(cross / cross_len)
        dot = float(np.clip(np.dot(source_dir, target_dir), -1.0, 1.0))
        angle = float(np.degrees(np.arccos(dot)))

    # STEP 2 — TRANSLATION:
    rotated_source_pos = rotate_vector(
        source_conn["position"], rotation_axis, angle
    )
    translation = np.array(target_conn["position"]) - rotated_source_pos

    return {
        "rotation_axis":     rotation_axis,
        "rotation_angle_deg": angle,
        "translation":        tuple(translation),
    }

def apply_transform(solid, transform: dict):
    """
    Apply transform to a CadQuery solid.
    ORDER: rotate first around world origin, then translate.
    """
    import cadquery as cq
    axis  = transform["rotation_axis"]
    angle = transform["rotation_angle_deg"]
    tx, ty, tz = transform["translation"]

    result = solid
    if abs(angle) > 1e-6:
        result = result.rotate((0,0,0), axis, angle)
    result = result.translate((tx, ty, tz))
    return result

def apply_transform_to_connector(connector: dict, transform: dict) -> dict:
    """
    Apply same transform to a connector dict (position + axis).
    Used to keep live_connectors in sync after each part is moved.
    """
    axis  = transform["rotation_axis"]
    angle = transform["rotation_angle_deg"]
    tx, ty, tz = transform["translation"]

    new_pos  = rotate_vector(connector["position"], axis, angle)
    new_pos  = tuple(new_pos + np.array([tx, ty, tz]))
    new_axis = tuple(rotate_vector(connector["axis"], axis, angle))

    return {**connector, "position": new_pos, "axis": new_axis}
