import os
import streamlit as st

def read_xyz_file(file_path):
    """
    Reads an XYZ file and extracts the atomic coordinates and element symbols.
    """
    with open(file_path, 'r') as f:
        lines = f.readlines()
    num_atoms = int(lines[0])
    coordinates = []
    for line in lines[2:]:
        parts = line.split()
        if len(parts) == 4:
            coordinates.append(parts)
    return num_atoms, coordinates

def write_xyz_file(file_path, num_atoms, coordinates):
    """
    Writes atomic coordinates to an XYZ file.
    """
    with open(file_path, 'w') as f:
        f.write(f"{num_atoms}\n")
        f.write("Generated polymer chain\n")
        for atom in coordinates:
            f.write(f"{atom[0]} {atom[1]} {atom[2]} {atom[3]}\n")

def create_polymer_chain(monomer_path, n_units, output_path):
    """
    Creates a polymer chain by repeating the monomer structure.

    Parameters:
    - monomer_path: str, path to the input monomer XYZ file.
    - n_units: int, number of monomer units in the polymer.
    - output_path: str, path to save the output polymer XYZ file.
    """
    num_atoms, monomer_coordinates = read_xyz_file(monomer_path)
    polymer_coordinates = []
    translation_vector = [0.0, 0.0, 0.0]

    for i in range(n_units):
        for atom in monomer_coordinates:
            x, y, z = float(atom[1]), float(atom[2]), float(atom[3])
            x += translation_vector[0]
            y += translation_vector[1]
            z += translation_vector[2]
            polymer_coordinates.append([atom[0], f"{x:.6f}", f"{y:.6f}", f"{z:.6f}"])
        translation_vector[2] += 3.0  # Increase z-axis for next monomer

    total_atoms = num_atoms * n_units
    write_xyz_file(output_path, total_atoms, polymer_coordinates)

# Streamlit interface
st.title("Polymer Constructor")

# Upload monomer file
monomer_file = st.file_uploader("Upload Monomer File (XYZ format)", type="xyz")

# Input number of units
n_units = st.number_input("Number of monomer units", min_value=1, step=1, value=5)

# Specify output file name
output_file_name = st.text_input("Output file name", value="polymer.xyz")

if monomer_file is not None and st.button("Generate Polymer"):
    monomer_path = "temp_monomer.xyz"
    with open(monomer_path, "wb") as f:
        f.write(monomer_file.read())

    if os.path.exists(monomer_path):
        create_polymer_chain(monomer_path, n_units, output_file_name)
        st.success(f"Polymer chain with {n_units} units created and saved as {output_file_name}.")

        # Display the output file content
        with open(output_file_name, "r") as f:
            st.text(f.read())

        # Remove temporary monomer file
        os.remove(monomer_path)
    else:
        st.error("Failed to process the uploaded monomer file.")

