import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import loadmat
import re
from photonflux import get_incident_photons

# === Config ===
folder = r"C:/Users/Admin/OneDrive - epfl.ch/Desktop/kerim analysis/2307/chip3_test_2"
mat_file = os.path.join(folder, "Cal_Phoenix3_2025_23_07_1940_400_20_500_SMU02_Ch1.mat")
calib_file = r"C:/Users/Admin/OneDrive - epfl.ch/Desktop/kerim analysis/Hamamatsu_Resp_320_5_960.xlsx"
target_voltage = 22.0
target_exposure = 1500
area = 19.63  # µm²

# === Get incident photon flux ===
wl_list, photonflux_list = get_incident_photons(mat_file, calib_file)
photonflux_dict = dict(zip(wl_list, photonflux_list))

# === Load DCR 2D map (pixel-wise) ===
dcr_map = None
for fname in os.listdir(folder):
    if fname.startswith("DCR") and fname.endswith(".mat"):
        match = re.search(r"DCR_\d+_(\d{2,3}(?:\.\d+)?)_(\d+)\.mat", fname)
        if match:
            voltage = float(match.group(1))
            exposure = int(match.group(2))
            if voltage == target_voltage and exposure == target_exposure:
                dcr_mat = loadmat(os.path.join(folder, fname))
                varname = [k for k in dcr_mat if not k.startswith("__")][0]
                dcr_map = dcr_mat[varname]
                dcr_map = np.nan_to_num(dcr_map)
                break

if dcr_map is None:
    raise ValueError("No DCR map found for the given voltage and exposure.")

# === Loop through LCR files and generate PDP maps ===
for fname in os.listdir(folder):
    if fname.startswith("LCR") and fname.endswith(".mat"):
        match = re.search(r"LCR_\d+_(\d{2,3}(?:\.\d+)?)_(\d+?)_(\d+)\.mat", fname)
        if match:
            voltage = float(match.group(1))
            wavelength = int(match.group(2))
            exposure = int(match.group(3))

            if voltage == target_voltage and exposure == target_exposure:
                if wavelength not in photonflux_dict:
                    print(f"[SKIP] No photon flux for {wavelength} nm")
                    continue

                # Load 2D LCR data
                path = os.path.join(folder, fname)
                mat = loadmat(path)
                varname = [k for k in mat if not k.startswith('__')][0]
                lcr_map = mat[varname]
                lcr_map = np.nan_to_num(lcr_map)

                if lcr_map.shape != dcr_map.shape:
                    print(f"[SKIP] Shape mismatch in {fname}")
                    continue

                # Compute PDP map (pixel-wise), clip to [0, 50]
                photon_in = photonflux_dict[wavelength]
                pdp_map = (lcr_map - dcr_map) / photon_in
                pdp_map = np.clip(pdp_map * 100, 0, 10)

                # Median PDP for info
                median_pdp = np.median(pdp_map[~np.isnan(pdp_map)])
                mean_pdp = np.mean(pdp_map[~np.isnan(pdp_map)])
                max_pdp = np.max(pdp_map[~np.isnan(pdp_map)])
                min_pdp = np.min(pdp_map[~np.isnan(pdp_map)])
                print(f"[INFO] Median PDP at {wavelength} nm = {median_pdp:.2f}%")

                # Rotate PDP map for display
                pdp_map_rot = pdp_map.T  # rotate 90°

                # Plot
                nrows, ncols = pdp_map_rot.shape
                scale = 0.1  # pixel scaling for size
                plt.figure(figsize=(ncols * scale, nrows * scale))
                plt.imshow(pdp_map_rot, cmap='viridis', vmin=0, vmax=10, interpolation='nearest')
                plt.colorbar(label='PDP (%)', shrink=0.75)
                plt.title(f'PDP Heatmap @ {wavelength} nm\nMedian PDP = {median_pdp:.2f}%')
                plt.xlabel('X pixels')
                plt.ylabel('Y pixels')
                plt.gca().set_aspect('equal')
                plt.tight_layout()
                plt.show()
