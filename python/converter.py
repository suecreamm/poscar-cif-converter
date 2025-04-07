import math
import re

def vector_norm(v):
    return math.sqrt(sum(x**2 for x in v))

def dot_product(v1, v2):
    return sum(x*y for x, y in zip(v1, v2))

def angle_between(v1, v2):
    dot = dot_product(v1, v2)
    norm1 = vector_norm(v1)
    norm2 = vector_norm(v2)
    cos_angle = dot / (norm1 * norm2)
    cos_angle = max(min(cos_angle, 1.0), -1.0)
    return math.degrees(math.acos(cos_angle))

def poscar_to_cif(poscar):
    lines = poscar.strip().splitlines()
    title = lines[0]
    scale = float(lines[1].strip())
    lattice = [list(map(float, lines[i].split())) for i in range(2, 5)]
    a_vec, b_vec, c_vec = [[scale * x for x in v] for v in lattice]

    a_len = vector_norm(a_vec)
    b_len = vector_norm(b_vec)
    c_len = vector_norm(c_vec)

    alpha = angle_between(b_vec, c_vec)
    beta = angle_between(a_vec, c_vec)
    gamma = angle_between(a_vec, b_vec)

    atom_types = lines[5].split()
    atom_counts = list(map(int, lines[6].split()))
    coord_start = 8
    coords = [list(map(float, lines[i].split()[:3])) for i in range(coord_start, coord_start + sum(atom_counts))]

    cif_lines = []
    cif_lines.append(f"{title.replace(' ', '_')}")
    cif_lines.append("_symmetry_space_group_name_H-M   'P 1'")
    cif_lines.append("_symmetry_Int_Tables_number      1")
    cif_lines.append(f"_cell_length_a    {a_len:.6f}")
    cif_lines.append(f"_cell_length_b    {b_len:.6f}")
    cif_lines.append(f"_cell_length_c    {c_len:.6f}")
    cif_lines.append(f"_cell_angle_alpha {alpha:.2f}")
    cif_lines.append(f"_cell_angle_beta  {beta:.2f}")
    cif_lines.append(f"_cell_angle_gamma {gamma:.2f}")
    cif_lines.append("loop_")
    cif_lines.append("  _atom_site_label")
    cif_lines.append("  _atom_site_fract_x")
    cif_lines.append("  _atom_site_fract_y")
    cif_lines.append("  _atom_site_fract_z")

    idx = 0
    for atom, count in zip(atom_types, atom_counts):
        for i in range(count):
            x, y, z = coords[idx]
            cif_lines.append(f"  {atom}{i+1} {x:.6f} {y:.6f} {z:.6f}")
            idx += 1

    return "\n".join(cif_lines)

def cif_to_poscar(cif):
    lines = cif.strip().splitlines()
    
    title = lines[0]
    if title.startswith("data_"):
        title = title[5:]
    
    a = b = c = 1.0
    alpha = beta = gamma = 90.0
    
    atoms_data = []
    in_loop = False
    columns = []
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        
        if re.search(r'[_*]cell[_*]length_a', line):
            a = float(line.split()[-1])
        elif re.search(r'[_*]cell[_*]length_b', line):
            b = float(line.split()[-1])
        elif re.search(r'[_*]cell[_*]length_c', line):
            c = float(line.split()[-1])
        elif re.search(r'[_*]cell[_*]angle_alpha', line):
            alpha = float(line.split()[-1])
        elif re.search(r'[_*]cell[_*]angle_beta', line):
            beta = float(line.split()[-1])
        elif re.search(r'[_*]cell[_*]angle_gamma', line):
            gamma = float(line.split()[-1])
        
        elif line.startswith("loop_"):
            in_loop = True
            columns = []
            continue
        
        elif in_loop and (line.startswith("_") or line.startswith("*")):
            columns.append(line)
        
        elif in_loop and not (line.startswith("_") or line.startswith("*") or line.startswith("loop_")):
            values = line.split()
            if len(values) >= 4:
                atoms_data.append(values)
    
    type_idx = -1
    x_idx = -1
    y_idx = -1
    z_idx = -1
    
    for i, col in enumerate(columns):
        if "type_symbol" in col:
            type_idx = i
        elif "fract_x" in col:
            x_idx = i
        elif "fract_y" in col:
            y_idx = i
        elif "fract_z" in col:
            z_idx = i
    
    label_idx = -1
    if type_idx == -1:
        for i, col in enumerate(columns):
            if "label" in col:
                label_idx = i
                break
    
    species = {}
    coords = []
    
    for data in atoms_data:
        if type_idx != -1 and type_idx < len(data):
            element = data[type_idx]
        elif label_idx != -1 and label_idx < len(data):
            element = ''.join(c for c in data[label_idx] if not c.isdigit())
        else:
            continue
        
        if x_idx != -1 and y_idx != -1 and z_idx != -1 and x_idx < len(data) and y_idx < len(data) and z_idx < len(data):
            try:
                x = float(data[x_idx])
                y = float(data[y_idx])
                z = float(data[z_idx])
                coords.append([x, y, z])
                species[element] = species.get(element, 0) + 1
            except ValueError:
                continue
    
    poscar = f"{title}\n1.0\n"
    
    poscar += f"{a:.6f} 0.0 0.0\n"
    poscar += f"0.0 {b:.6f} 0.0\n"
    poscar += f"0.0 0.0 {c:.6f}\n"
    
    poscar += " ".join(species.keys()) + "\n"
    poscar += " ".join(str(v) for v in species.values()) + "\n"
    
    poscar += "Direct\n"
    for coord in coords:
        poscar += f"{coord[0]:.6f} {coord[1]:.6f} {coord[2]:.6f}\n"
    
    return poscar

__all__ = ['poscar_to_cif', 'cif_to_poscar', 'vector_norm', 'dot_product', 'angle_between']
