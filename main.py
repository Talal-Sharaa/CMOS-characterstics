import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Define NMOS and PMOS constants (with defaults)
Kn = 1e-3
Kp = 2e-3
Vth = 1 

# Define Vgs sweep range and points
Vgs_points = 21

# Define Vds range and points
Vds_points = 101

# Function to calculate NMOS drain current 
def nmos_Ids(Vgs, Vds):
    if Vgs < Vth:
        return np.zeros_like(Vds)
    else:
        return Kn * (2 * (Vgs - Vth) * Vds - Vds**2) / (Vgs - Vth)

# Function to calculate PMOS drain current (shifted and flipped)
def pmos_Ids(Vgs, Vds):
    Vgs_shifted = Vgs - Vth
    Vds_shifted = Vds - Vth
    if Vgs_shifted < 0:
        return np.zeros_like(Vds)
    else:
        return -Kp * (2 * (Vgs_shifted) * Vds_shifted - Vds_shifted**2) / (Vgs_shifted)

# User input section with error handling
st.title("Ids vs Vds Transistor Tool")

Kn = st.number_input("Enter Kn:", value=Kn)
Kp = st.number_input("Enter Kp:", value=Kp)
Vth = st.number_input("Enter Vth:", value=Vth)

vgs_mode = st.radio("Select Vgs mode:", options=["Sweep", "Single value"])
Vgs_max = 0
Vgs_min = 0  # Define Vgs_min here

if vgs_mode == "Sweep":
    Vgs_min = st.number_input("Enter Vgs min:", value=Vth - 2)
    Vgs_max = st.number_input("Enter Vgs max:", value=5)
else:  
    single_vgs = st.number_input("Enter Vgs value:", value=Vth + 1) 

Vds_min = st.number_input("Enter Vds min:", value=0)
Vds_max = st.number_input("Enter Vds max:", value=10)

# Error handling
if Kn <= 0 or Kp <= 0:
    st.error("Kn and Kp must be positive values")
elif Vth <= 0:
    st.error("Vth must be a positive value")
elif Vgs_max <= Vgs_min and vgs_mode == "Sweep":
    st.error("Vgs max must be greater than Vgs min")
elif Vds_max <= Vds_min:
    st.error("Vds max must be greater than Vds min")
else:
# Calculation and plotting logic if no errors
    if vgs_mode == "Sweep":
        Vgs = np.linspace(Vgs_min, Vgs_max, Vgs_points)
    else:
        Vgs = np.array([single_vgs])  
    Vds = np.linspace(Vds_min, Vds_max, Vds_points)

# Create plots for NMOS and PMOS
    plt.figure(figsize=(10, 6))

    # NMOS plot
    for vgs in Vgs:
        Ids_nmos = nmos_Ids(vgs, Vds)
        plt.plot(Vds, Ids_nmos, label=f'Vgs_NMOS = {vgs:.2f}V')

    # PMOS plot (shifted and flipped)
    for vgs in np.flip(Vgs):
        Ids_pmos = pmos_Ids(vgs, Vds)
        plt.plot(Vds, Ids_pmos, label=f'Vgs_PMOS = {vgs:.2f}V')

    # Plot labels and title
    plt.xlabel('Vds (V)')
    plt.ylabel('Ids (A)')
    plt.title('Ids vs Vds for NMOS and PMOS (shifted and flipped PMOS)')
    plt.grid(True)
    plt.legend()

    st.pyplot(plt.gcf())
