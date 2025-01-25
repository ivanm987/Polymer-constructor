import numpy as np
import streamlit as st
import py3Dmol
from io import StringIO

def write_xyz_string(num_atoms, coordinates):
    """
    Writes atomic coordinates to an XYZ format string.
    """
    output = StringIO()
    output.write(f"{num_atoms}\n")
    output.write("Generated polymer chain\n")
    for atom in coordinates:
        output.write(f"{atom[0]} {atom[1]} {atom[2]} {atom[3]}\n")
    return output.getvalue()

def create_polymer_chain(n_units, bond_angle, torsion_angle, bond_length, monomer_type):
    """
    Creates a polymer chain by generating spheres connected at specified angles.

    Parameters:
    - n_units: int, number of monomer units in the polymer.
    - bond_angle: float, angle in degrees between consecutive bonds.
    - torsion_angle: float, torsion angle in degrees for 3D rotation.
    - bond_length: float, distance between monomers.
    - monomer_type: str, type of monomer (e.g., C, O, N).

    Returns:
    - num_atoms: int, total number of atoms in the polymer.
    - coordinates: list, atomic coordinates in XYZ format.
    - bonds: list, pairs of atom indices representing bonds.
    """
    coordinates = []
    bonds = []
    x, y, z = 0.0, 0.0, 0.0
    angle = 0.0
    torsion = 0.0

    for i in range(n_units):
        # Add the current monomer as a sphere (single atom for simplicity)
        coordinates.append([monomer_type, f"{x:.6f}", f"{y:.6f}", f"{z:.6f}"])

        # Create bond to previous monomer
        if i > 0:
            bonds.append((i - 1, i))

        # Update position for the next monomer
        angle_rad = np.radians(angle)
        torsion_rad = np.radians(torsion)
        x += bond_length * np.cos(angle_rad) * np.cos(torsion_rad)
        y += bond_length * np.sin(angle_rad) * np.cos(torsion_rad)
        z += bond_length * np.sin(torsion_rad)

        # Update angles for the next iteration
        angle += bond_angle
        torsion += torsion_angle

    num_atoms = n_units
    return num_atoms, coordinates, bonds

def visualize_polymer(coordinates, bonds):
    """
    Visualize the polymer using py3Dmol.
    """
    view = py3Dmol.view(width=800, height=400)

    # Add atoms
    for i, atom in enumerate(coordinates):
        view.addSphere({
            "center": {
                "x": float(atom[1]),
                "y": float(atom[2]),
                "z": float(atom[3])
            },
            "radius": 0.3,
            "color": "blue" if atom[0] == "N" else "gray"
        })

    # Add bonds
    for bond in bonds:
        start = coordinates[bond[0]]
        end = coordinates[bond[1]]
        view.addCylinder({
            "start": {
                "x": float(start[1]),
                "y": float(start[2]),
                "z": float(start[3])
            },
            "end": {
                "x": float(end[1]),
                "y": float(end[2]),
                "z": float(end[3])
            },
            "radius": 0.1,
            "color": "gray"
        })

    view.zoomTo()
    return view

# Streamlit interface
st.title("Polymer Constructor")

# Input parameters
n_units = st.number_input("Number of monomer units", min_value=1, step=1, value=5)
bond_angle = st.slider("Bond angle (degrees)", min_value=0, max_value=180, value=120, step=1)
torsion_angle = st.slider("Torsion angle (degrees)", min_value=-180, max_value=180, value=0, step=1)
bond_length = st.slider("Bond length (angstroms)", min_value=0.5, max_value=5.0, value=1.5, step=0.1)
monomer_type = st.selectbox("Monomer type", ["C", "O", "N", "H"])

# Generate polymer chain
if st.button("Generate Polymer"):
    num_atoms, coordinates, bonds = create_polymer_chain(n_units, bond_angle, torsion_angle, bond_length, monomer_type)
    xyz_content = write_xyz_string(num_atoms, coordinates)

    # Display XYZ content
    st.text_area("Generated Polymer (XYZ Format)", xyz_content, height=300)

    # Visualize polymer
    st.subheader("Polymer Visualization")
    view = visualize_polymer(coordinates, bonds)
    st.components.v1.html(view._make_html(), height=500)

    # Download option
    st.download_button(
        label="Download Polymer XYZ File",
        data=xyz_content,
        file_name="polymer.xyz",
        mime="text/plain"
    )


