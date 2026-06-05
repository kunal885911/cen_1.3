from core.generator import generate_model_bundle
from schemas.assembly_machine_params import AssemblyMachineParams


def generate_assembly_machine_step_file(params_dict: dict, step_path: str):
    """Generate 9-part Assembly Machine STEP file"""
    try:
        import cadquery as cq  # type: ignore
        
        base_plate_length = params_dict.get("base_plate_length", 500.0)
        base_plate_width = params_dict.get("base_plate_width", 300.0)
        wheel_diameter = params_dict.get("wheel_diameter", 250.0)
        
        # PART-01: Base Plate
        base_plate = cq.Workplane("XY").box(base_plate_length, base_plate_width, 20)
        xs = [-base_plate_length/2 + 40, -base_plate_length/2 + 220, -base_plate_length/2 + 410]
        ys = [-base_plate_width/2 + 85, -base_plate_width/2 + 215]
        pts = [(x, y) for x in xs for y in ys]
        base_plate = base_plate.faces(">Z").workplane().pushPoints(pts).hole(9.0).edges().chamfer(0.5)
        
        # PART-02: Support Blocks (2x)
        support_block = cq.Workplane("XY").box(100, 100, 80)
        support_block = support_block.faces(">Z").workplane().pushPoints([(-40, 40), (40, -40)]).hole(9.0)
        support_block = support_block.faces(">Z").workplane().cboreHole(14.0, 20.0, 12.6)
        support_block = support_block.edges().chamfer(0.5)
        support_block_front = support_block.translate((-200, -100, 20))
        support_block_back = support_block.translate((200, -100, 20))
        
        # PART-03: Stepped Shaft
        large = cq.Workplane("XY").cylinder(20, 25).translate((0, 0, 10))
        small = cq.Workplane("XY").cylinder(30, 20).translate((0, 0, 35))
        stepped_shaft = large.union(small).edges().chamfer(0.5).translate((0, 150, 100))
        # Rotate 90 degrees around Z axis
        stepped_shaft = stepped_shaft.rotate((0, 0, 0), (0, 0, 1), 90)
        
        # PART-04: Wheel
        wheel = cq.Workplane("XY").cylinder(30, wheel_diameter/2).faces(">Z").workplane().hole(40)
        wheel = wheel.edges().chamfer(0.5).translate((0, 150, 80))
        # Rotate 90 degrees around Z axis
        wheel = wheel.rotate((0, 0, 0), (0, 0, 1), 90)
        
        # PART-05: Threaded Shaft
        shaft_main = cq.Workplane("XY").cylinder(35, 10).translate((0, 0, 17.5))
        flange = cq.Workplane("XY").cylinder(5, 15).translate((0, 0, 37.5))
        threaded_shaft = shaft_main.union(flange).faces(">Z").workplane().hole(6.8, 15.0)
        threaded_shaft = threaded_shaft.edges().chamfer(0.5).translate((0, -150, 100))
        
        # PART-06: Slotted Plate
        plate = cq.Workplane("XY").box(50, 350, 20)
        plate = plate.faces(">Z").workplane().center(0, -150).hole(20.0)
        plate = plate.faces(">Z").workplane().center(0, 150).hole(25.0)
        plate = plate.edges().chamfer(0.5).translate((0, 0, 50))
        
        # PART-07: Side Blocks (2x)
        side = cq.Workplane("XZ").box(220, 75, 135)
        cut = cq.Workplane("XZ").box(230, 30, 20).translate((0, 22.5, 45))
        side = side.cut(cut).faces("<Y").workplane().pushPoints([(-100, 12.5), (100, 12.5)]).hole(6.8, 33.8)
        side = side.edges().chamfer(0.5)
        side_left = side.translate((-200, -100, 100))
        side_right = side.translate((200, -100, 100))
        
        # PART-08: Top Plate
        pts_trapz = [(-50, -10), (50, -10), (40, 10), (-50, 10)]
        top = cq.Workplane("XZ").polyline(pts_trapz).close().extrude(70, both=True)
        top = top.faces(">Z").workplane().hole(9.0)
        top = top.edges().chamfer(0.5).translate((0, 0, 180))
        
        # PART-09: Shaft 3
        shaft3 = cq.Workplane("XY").cylinder(25, 12.5).faces(">Z").workplane().hole(8)
        shaft3 = shaft3.edges().chamfer(0.5).translate((0, 0, 130))
        
        # Assemble
        assembly = base_plate.union(support_block_front).union(support_block_back)
        assembly = assembly.union(stepped_shaft).union(wheel)
        assembly = assembly.union(threaded_shaft).union(plate)
        assembly = assembly.union(side_left).union(side_right)
        assembly = assembly.union(top).union(shaft3)
        
        # Export to STEP
        cq.exporters.export(assembly, str(step_path), "STEP")
        
    except Exception as exc:
        print("ERROR IN PROCESS:", exc)
        raise exc


def assembly_machine_logs(params: AssemblyMachineParams) -> list[str]:
    """Generate log messages for assembly machine"""
    return [
        f"Assembly Machine generated successfully",
        f"Base Plate: {params.base_plate_length}×{params.base_plate_width}mm",
        f"Wheel Diameter: {params.wheel_diameter}mm",
        f"9 components assembled",
    ]


async def generate_assembly_machine(params: AssemblyMachineParams) -> dict:
    """Generate 9-part Assembly Machine STEP file"""
    return await generate_model_bundle(
        model_name="assembly_machine",
        params=params,
        step_generator=generate_assembly_machine_step_file,
        log_builder=assembly_machine_logs,
    )
