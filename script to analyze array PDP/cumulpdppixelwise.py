# pdp_cumul_by_wavelength_pixelwise.py

import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import loadmat
import re
from photonflux import get_incident_photons
# === Config ===
folder = r"C:/Users/Admin/OneDrive - epfl.ch/Desktop/kerim analysis/2708/PDP/chip3_AI_#3"
mat_file = r"C:/Users/Admin/OneDrive - epfl.ch/Desktop/kerim analysis/2708/PDP/chip3_AI_#3/Cal_Phoenix3_2025_27_08_0945_320_20_960_SMU02_Ch1.mat"
calib_file = r"C:/Users/Admin/OneDrive - epfl.ch/Desktop/kerim analysis/Hamamatsu_Resp_320_5_960.xlsx"
area = 19.63  # µm²
target_voltage = 22.0

# === Get incident photon flux ===
wl_list, photonflux_list = get_incident_photons(mat_file, calib_file)
photonflux_dict = dict(zip(wl_list, photonflux_list))

# === Collect PDP CDFs per wavelength ===
pdp_cdfs = {}  # wavelength → sorted PDP array

for fname in os.listdir(folder):
    if not fname.endswith(".mat"):
        continue

    match = re.search(r"LCR_\d+_(\d{2,3}(?:\.\d+)?)_(\d+?)_(\d+)\.mat", fname)
    if match:
        voltage = float(match.group(1))
        wavelength = int(match.group(2))
        exposure = int(match.group(3))

        if voltage == target_voltage:
            # --- Load LCR 2D ---
            path = os.path.join(folder, fname)
            mat = loadmat(path)
            varname = [k for k in mat if not k.startswith('__')][0]
            lcr_2d = mat[varname]
            lcr_2d = np.nan_to_num(lcr_2d)

            # --- Load matching DCR 2D ---
            # --- Try to find matching DCR file with same voltage ---
            dcr_2d = None
            for dname in os.listdir(folder):
                if dname.startswith("DCR") and dname.endswith(".mat"):
                    dcr_match = re.search(r"DCR_\d+_(\d{2,3}(?:\.\d+)?)_\d+\.mat", dname)
                    if dcr_match:
                        dcr_voltage = float(dcr_match.group(1))
                        if np.isclose(dcr_voltage, voltage):  # use isclose to avoid float mismatch
                            dmat = loadmat(os.path.join(folder, dname))
                            varname = [k for k in dmat if not k.startswith('__')][0]
                            dcr_2d = np.nan_to_num(dmat[varname])
                            break


            # --- Compute PDP array ---
            if dcr_2d is not None and lcr_2d.shape == dcr_2d.shape and wavelength in photonflux_dict:
                photon_in = photonflux_dict[wavelength]
                pdp_map = (lcr_2d - dcr_2d) / photon_in
                pdp_map = np.clip(pdp_map, 0, None)
                pdp_flat = pdp_map.flatten() * 100  # convert to %
                print('Median', np.median(pdp_flat))
                sorted_pdp = np.sort(pdp_flat)
                pdp_cdfs[wavelength] = sorted_pdp

# === Plot all CDFs ===
plt.figure(figsize=(10, 7))
for wl in sorted(pdp_cdfs):
    sorted_pdp = pdp_cdfs[wl]
    percent = np.linspace(0, 100, len(sorted_pdp))
    plt.plot(percent, sorted_pdp, label=f"{wl} nm")

plt.xlabel("Cumulative %", fontsize = 16)
plt.ylabel("PDP (%)", fontsize = 16)
plt.yscale("log")  # optional
plt.xticks(fontsize=14); plt.yticks(fontsize=14)
#plt.xlim(99.25, 100.05)  # adjust if needed
plt.ylim(5e-1,5e2)
plt.title(f"CDF of PDP at {target_voltage} V", fontsize = 16)
plt.grid(True)
plt.legend(title="Wavelength", fontsize = 12)
plt.tight_layout()
plt.show()

# === Extract median PDP per wavelength ===
median_pdp = {wl: np.median(pdp_cdfs[wl]) for wl in pdp_cdfs}
wavelengths_sorted = sorted(median_pdp.keys())
medians_sorted = [median_pdp[wl] for wl in wavelengths_sorted]

# === Plot median PDP vs wavelength ===
plt.figure(figsize=(10,7))
plt.plot(wavelengths_sorted, medians_sorted, marker='o')
plt.xticks(fontsize=16); plt.yticks(fontsize=16)
plt.xlabel("Wavelength (nm)", fontsize = 18)
plt.ylabel("Median PDP (%)", fontsize = 18)
plt.title(f"Median PDP vs Wavelength at {target_voltage} V", fontsize = 18)
plt.grid(True)
plt.tight_layout()
plt.show()