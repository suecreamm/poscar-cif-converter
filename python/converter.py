# Import required libraries
import math

# Utility functions
def vector_norm(v):
    """
    Calculate the Euclidean norm of a vector
    
    Args:
        v (list): Vector coordinates
        
    Returns:
        float: The magnitude of the vector
    """
    return math.sqrt(sum(x**2 for x in v))

def dot_product(v1, v2):
    """
    Calculate the dot product of two vectors
    
    Args:
        v1 (list): First vector
        v2 (list): Second vector
        
    Returns:
        float: Dot product value
    """
    return sum(x*y for x, y in zip(v1, v2))

def angle_between(v1, v2):
    """
    Calculate the angle between two vectors in degrees
    
    Args:
        v1 (list): First vector
        v2 (list): Second vector
        
    Returns:
        float: Angle in degrees
    """
    dot = dot_product(v1, v2)
    norm1 = vector_norm(v1)
    norm2 = vector_norm(v2)
    cos_angle = dot / (norm1 * norm2)
    cos_angle = max(min(cos_angle, 1.0), -1.0)
    return math.degrees(math.acos(cos_angle))

def poscar_to_cif(poscar):
    """
    Convert POSCAR format to CIF format
    
    Args:
        poscar (str): Content of POSCAR file
        
    Returns:
        str: Converted CIF content
    """
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
    # Use title without data_ prefix as requested
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
    """
    Convert CIF format to POSCAR format
    
    Args:
        cif (str): Content of CIF file
        
    Returns:
        str: Converted POSCAR content
    """
    lines = cif.strip().splitlines()
    # Extract title, handling both cases (with or without data_ prefix)
    title = lines[0]
    if title.startswith("data_"):
        title = title[5:]
    
    a = b = c = 1
    alpha = beta = gamma = 90
    atom_lines = []
    reading_atoms = False
    
    for line in lines:
        if "_cell_length_a" in line:
            a = float(line.split()[-1])
        elif "_cell_length_b" in line:
            b = float(line.split()[-1])
        elif "_cell_length_c" in line:
            c = float(line.split()[-1])
        elif line.strip().startswith("loop_"):
            reading_atoms = False
        elif "_atom_site_fract_z" in line:
            reading_atoms = True
            atom_lines = []
        elif reading_atoms and line.strip() and not line.strip().startswith("_"):
            atom_lines.append(line.strip())

    species = {}
    coords = []
    for line in atom_lines:
        tokens = line.split()
        label = tokens[0]
        sym = ''.join(filter(str.isalpha, label))
        species[sym] = species.get(sym, 0) + 1
        coords.append([float(x) for x in tokens[1:4]])

    poscar = f"{title}\n1.0\n"
    poscar += f"{a:.6f} 0.0 0.0\n"
    poscar += f"0.0 {b:.6f} 0.0\n"
    poscar += f"0.0 0.0 {c:.6f}\n"
    poscar += " ".join(species.keys()) + "\n"
    poscar += " ".join(str(v) for v in species.values()) + "\n"
    poscar += "Direct\n"
    for c in coords:
        poscar += f"{c[0]:.6f} {c[1]:.6f} {c[2]:.6f}\n"
    return poscar

# Define which functions should be available when imported
__all__ = ['poscar_to_cif', 'cif_to_poscar', 'vector_norm', 'dot_product', 'angle_between']
