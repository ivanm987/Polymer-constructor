import numpy as np
import streamlit as st
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

def create_polymer_chain(n_units, bond_angle, rigidity):
    """
    Creates a polymer chain by generating spheres connected at specified angles.

    Parameters:
    - n_units: int, number of monomer units in the polymer.
    - bond_angle: float, angle in degrees between consecutive bonds.
    - rigidity: float, controls deviation from the bond angle (0 = rigid).

    Returns:
    - num_atoms: int, total number of atoms in the polymer.
    - coordinates: list, atomic coordinates in XYZ format.
    """
    coordinates = []
    x, y, z = 0.0, 0.0, 0.0
    angle = 0.0

    for i in range(n_units):
        # Add the current monomer as a sphere (single atom for simplicity)
        coordinates.append(["C", f"{x:.6f}", f"{y:.6f}", f"{z:.6f}"])

        # Update position for the next monomer
        angle_rad = np.radians(angle)
        x += np.cos(angle_rad)
        y += np.sin(angle_rad)
        z += 1.0  # Linear progression along z-axis

        # Introduce variability based on rigidity
        angle += bond_angle + np.random.uniform(-rigidity, rigidity)

    num_atoms = n_units
    return num_atoms, coordinates

# Streamlit interface
st.title("Polymer Constructor")

# Input parameters
n_units = st.number_input("Number of monomer units", min_value=1, step=1, value=5)
bond_angle = st.slider("Bond angle (degrees)", min_value=0, max_value=180, value=120, step=1)
rigidity = st.slider("Rigidity (0 = rigid, higher = flexible)", min_value=0.0, max_value=10.0, value=0.0, step=0.1)

# Generate polymer chain
if st.button("Generate Polymer"):
    num_atoms, coordinates = create_polymer_chain(n_units, bond_angle, rigidity)
    xyz_content = write_xyz_string(num_atoms, coordinates)

    # Display XYZ content
    st.text_area("Generated Polymer (XYZ Format)", xyz_content, height=300)

    # Download option
    st.download_button(
        label="Download Polymer XYZ File",
        data=xyz_content,
        file_name="polymer.xyz",
        mime="text/plain"
    )


