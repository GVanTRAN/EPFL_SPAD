import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import loadmat
import re
from photonflux import get_incident_photons

# === CONFIG ===
folder = r"C:/Users/Admin/OneDrive - epfl.ch/Desktop/kerim analysis/2708/PDPvsDCR/chip3_AI_#3"
mat_file = r"C:/Users/Admin/OneDrive - epfl.ch/Desktop/kerim analysis/2708/PDPvsDCR/chip3_AI_#3/Cal_Phoenix3_2025_27_08_0945_320_20_960_SMU02_Ch1.mat"
calib_file = r"C:/Users/Admin/OneDrive - epfl.ch/Desktop/kerim analysis/Hamamatsu_Resp_320_5_960.xlsx"
area = 19.63  # µm²
target_wavelength = 440  # nm

# === Get photon flux ===
wl_list, photonflux_list = get_incident_photons(mat_file, calib_file)
photonflux_dict = dict(zip(wl_list, photonflux_list))
photon_in = photonflux_dict.get(target_wavelength, None)
if photon_in is None:
    raise ValueError("Photon flux not found for target wavelength")

# === Match LCR and DCR by voltage ===
dcr_dict = {}
lcr_dict = {}

for fname in os.listdir(folder):
    if fname.endswith(".mat"):
        if fname.startswith("DCR"):
            m = re.search(r"DCR_\d+_(\d{2,3}(?:\.\d+)?)_(\d+)\.mat", fname)
            if m:
                v = float(m.group(1))
                dcr_dict[v] = os.path.join(folder, fname)

        elif fname.startswith("LCR"):
            m = re.search(r"LCR_\d+_(\d{2,3}(?:\.\d+)?)_(\d+?)_(\d+)\.mat", fname)
            if m:
                v = float(m.group(1))
                wl = int(m.group(2))
                exp = int(m.group(3))
                if wl == target_wavelength:
                    lcr_dict[v] = os.path.join(folder, fname)

# === Compute median DCR and PDP ===
common_voltages = sorted(set(dcr_dict.keys()) & set(lcr_dict.keys()))
med_dcr_list = []
med_pdp_list = []

for v in common_voltages:
    dcr = loadmat(dcr_dict[v])
    lcr = loadmat(lcr_dict[v])

    dcr_2d = dcr[[k for k in dcr if not k.startswith("__")][0]] 
    lcr_2d = lcr[[k for k in lcr if not k.startswith("__")][0]]

    net = np.clip(lcr_2d - dcr_2d, 0, None)
    pdp_2d = (net / photon_in) * 100

    # Flatten and clean
    dcr_flat = dcr_2d.flatten()
    pdp_flat = pdp_2d.flatten()
    mask = ~np.isnan(dcr_flat) & ~np.isnan(pdp_flat)

    med_dcr = np.median(dcr_flat[mask])
    med_pdp = np.median(pdp_flat[mask])

    med_dcr_list.append(med_dcr)
    med_pdp_list.append(med_pdp)

# === Plot ===
plt.figure(figsize=(8,6))
plt.plot(med_dcr_list, med_pdp_list, 'o-')
plt.xscale("log")
plt.xlabel("Median DCR (cps)", fontsize=14)
plt.ylabel("Median PDP (%)", fontsize=14)
plt.title("Median PDP vs DCR @ 440 nm", fontsize=16)
plt.grid(True, which="both", linestyle="--", linewidth=0.5)
#plt.legend()
plt.tight_layout()
plt.show()
