# CAD Engineer Platform Manual

Welcome to the **Parametric CAD Generation Platform**. This manual is designed specifically for CAD Engineers to understand how to utilize our dynamic assembly engine, configure parametric components, and successfully generate multi-part assemblies.

---

## 1. Introduction to the Platform

Our platform allows you to generate mathematically precise, production-ready 3D CAD models using a parametric configuration system. Instead of manually drawing geometry in traditional CAD software (like SolidWorks or Fusion360), you define dimensions and connection points (mates) through our interface or API, and the system automatically generates, assemblies, and packages the 3D files.

### Key Capabilities:
- **Dynamic Assembly Engine**: Define how multiple components connect, and the engine automatically calculates 3D spatial transformations and chained geometric positioning.
- **Physical Color System**: Every generated component type features a realistic CAD color (e.g., Brass Orange for certain parts, Steel Blue for others) to aid in visual identification within complex assemblies.
- **Triple-Output CAD Export**: For every assembly request, the system generates:
  1. `assembly_colored.step`: A true multi-body CAD assembly preserving individual parts and colors.
  2. `assembly_fused.step`: A boolean union (single solid) of the entire assembly, ideal for downstream CNC CAM operations or 3D printing.
  3. `part_*.step`: Isolated `.step` files for every individual component in the assembly.

---

## 2. The Component Library & Parameter Rules

To prevent physically impossible or structurally unstable CAD models, the platform enforces strict synchronous mathematical rules. 

> [!WARNING]
> If a parameter violates these physical constraints, the engine will block generation and return a validation error.

Here are the standard components available and their dimensional constraints:

### Shaft
- **Diameter**: `6mm` to `500mm`
- **Length**: `10mm` to `2000mm`
- **Design Rule**: To prevent structural failure and bending, Length cannot exceed 20× its Diameter.

### Plate
- **Length / Width**: `10mm` to `2000mm`
- **Design Rule**: To maintain structural rigidity, the aspect ratio (Length / Width) must be 4:1 or less.

### Flange
- **Inner Diameter**: `36mm` to `620mm`
- *Note: Outer diameter, thickness, and bolt hole arrays are parametrically driven by the inner diameter.*

### L-Bracket
- **Length 1 (L1) & Length 2 (L2)**: `10mm` to `1000mm`
- **Width (W)**: `10mm` to `500mm`
- **Design Rule**: Both L1 and L2 must be greater than or equal to the Width to ensure stability.

### U-Bracket
- **Length (L) / Height (H)**: `10mm` to `1000mm`
- **Width (W)**: `10mm` to `500mm`
- **Design Rule**: Base Length and Height must be greater than or equal to the Width.

### Housing
- **Dimensions (L, W, H)**: `20mm` to `2000mm`
- **Design Rule**: The derived wall thickness cannot consume more than 40% of the internal cavity space.

---

## 3. The Assembly Engine & Mating Rules

The core of the platform is the **Smart Connection Builder**. When building an assembly, you must connect valid geometric points (connectors) together. 

### Connector Reference Guide

The system uses a strict string-based naming convention: `part_id.connector_name`.

| Component Type | Valid Connectors | Description / Location |
| :--- | :--- | :--- |
| **Shaft** | `left_end` <br> `right_end` | Circular flat face on the left side (origin).<br>Circular flat face on the right side. |
| **Flange** | `back_center` <br> `front_center` <br> `bolt_holes` | Flat back face of the flange.<br>Flat front face of the flange.<br>Circular array of bolt holes. |
| **Plate** | `top_face` <br> `bottom_face` | Main upper surface.<br>Main lower surface. |
| **Housing** | `top_face`<br>`bottom_face`<br>`front_face` | Upper horizontal face.<br>Lower horizontal base.<br>Front vertical face. |
| **L-Bracket** | `face_1`<br>`face_2` | Horizontal base face.<br>Upright vertical wall face. |
| **U-Bracket** | `base_face`<br>`left_wall`<br>`right_wall` | Bottom flat base.<br>Inner/outer face of the left wall.<br>Inner/outer face of the right wall. |

### Smart Mating Logic

Just like physical mating in SolidWorks, connectors have "types" (Face, Cylindrical, Hole). The engine restricts connections to physically possible mates:

- **Cylindrical connectors** (e.g., Shaft ends) can mate with `Cylindrical`, `Hole`, and `Face`.
- **Face connectors** (e.g., Plate surfaces) can mate with `Face`, `Hole`, and `Cylindrical`.
- **Hole connectors** (e.g., Flange bolt holes) can mate with `Cylindrical` and `Face`.

> [!TIP]
> **Example Assembly Flow**
> To attach a Shaft (assigned ID: `1`) to the back of a Flange (assigned ID: `2`), you would map the connection as:
> `1.right_end` ↔ `2.back_center`
> The platform will automatically calculate the 3D translation matrix to snap these two faces perfectly together.

---

## 4. Platform Outputs & Artifacts

When an assembly generation is successful, the platform compiles a highly organized ZIP package for you to download. 

**What's inside the `.zip` export?**
- `assembly_colored.step`: The primary assembly file. Import this into your CAD software (SolidWorks, Inventor) or rendering engine (KeyShot) to view the complete multi-body model with colors intact.
- `assembly_fused.step`: A boolean union version of the assembly. Use this file if you are sending the assembly directly to a slicer for 3D printing.
- `part_{id}.step`: Individual geometry files for every single component in your assembly.
- `params.json`: A record of the exact dimensions and parameters used, ensuring perfect traceability.
- `color_legend.json`: A mapping of the colors applied to the parts.
- `logs.txt`: Generation logs, useful if you suspect a geometric anomaly.

---

## 5. Best Practices & Troubleshooting

- **Start Simple**: When designing complex chained assemblies (e.g., Shaft -> Flange -> Plate -> Bracket), build the connections linearly. Ensure part A connects to part B, then part B connects to part C.
- **Watch Validation Rules**: If generation fails, check the UI or `logs.txt` for validation errors. Most failures occur because an inputted parameter violated the maximum aspect ratios or mating rules.
- **Use Fused Models for CAM**: If you are using CAM software, prefer the `assembly_fused.step` to avoid issues with overlapping bodies. Use `assembly_colored.step` for rendering and design reviews.

---

## 6. Step-by-Step Guide: How to Use the App & Generate Assemblies

Follow these straightforward steps to create your first CAD assembly using our web application.

### Step 1: Start the Application
1. Run the platform by executing the provided startup script (`run_project.bat` on Windows) or starting the frontend and backend manually.
2. Open your web browser and navigate to the local application URL (typically `http://localhost:5173`).

### Step 2: Configure Your Assembly Details
1. On the main dashboard, locate the **Assembly Configuration** panel.
2. Enter an **Assembly Name** (e.g., `Motor_Drive_Assembly`).

### Step 3: Add Components
1. Click the **Add Component** button.
2. Select a component type from the dropdown (e.g., `shaft`, `flange`, `plate`).
3. The system will automatically assign it a unique ID (e.g., `1`, `2`).
4. **Set Parameters**: Input the specific dimensions for your component in the parameter fields provided. Remember to respect the **Design Rules** outlined in Section 2 (e.g., a shaft's length cannot exceed 20× its diameter).
5. Repeat this process until all parts for your assembly have been added.

### Step 4: Define the Mating Connections
1. Scroll down to the **Connections** panel.
2. Click **Add Connection** to define how two parts fit together.
3. **Select Part A and Connector A**: Choose the first component (e.g., `Part 1 (shaft)`) and select its connector point (e.g., `right_end`).
4. **Select Part B and Connector B**: The target connector dropdown is *smart*. It will automatically filter out incompatible mates. Select the target component (e.g., `Part 2 (flange)`) and choose a valid mating point (e.g., `back_center`).
5. Ensure all necessary connections are mapped to form a cohesive, unbroken chain of parts.

### Step 5: Select Export Modes & Generate
1. Check the desired export formats at the bottom of the form (e.g., `assembly`, `fused`, `individual_parts`).
2. Click the **Generate CAD** button.
3. The backend will process your request, validate the mathematics, and calculate the 3D geometry. 

### Step 6: Download & Inspect
1. Upon success, a `.zip` package will automatically download to your computer.
2. Extract the package and open `assembly_colored.step` in your preferred CAD software to inspect the generated assembly and its physical colors.
3. If an error occurs, the UI will display a specific validation message (e.g., "Geometry Failure") explaining exactly which parameter or connection was physically impossible.
