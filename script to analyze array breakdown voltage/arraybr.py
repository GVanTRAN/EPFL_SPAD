import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import loadmat
import re

# === Config ===
folder = r"C:/Users/Admin/OneDrive - epfl.ch/Desktop/kerim analysis/2508/chip1_AI_#1/br"
target_wavelength = 450
area = 19.63  # µm²
V_thre = 0.9 # V
threshold_cps = 0  # Activation threshold in cps/µm²

# === Collect and sort DCR files (room light case) ===
# === Collect and sort DCR files (all exposures) ===
dcr_files = []
for fname in os.listdir(folder):
    match = re.search(r'DCR_(\d+)_(\d{2,3}(?:\.\d+)?)_(\d+)\.mat', fname)
    if match:
        index = int(match.group(1))
        voltage = float(match.group(2))
        exposure = int(match.group(3))
        dcr_files.append((voltage, os.path.join(folder, fname)))

if not dcr_files:
    raise FileNotFoundError("No DCR files found in the folder.")

dcr_files.sort()  # increasing voltage


# === Build V_on map ===
Von_map = None

for voltage, path in dcr_files:
    mat = loadmat(path)
    varname = [k for k in mat if not k.startswith('__')][0]
    data = mat[varname]

    if Von_map is None:
        Von_map = np.full(data.shape, np.nan, dtype=np.float32)

    cps = data / area
    activation = (cps > threshold_cps) & np.isnan(Von_map)
    Von_map[activation] = voltage

# === Plot V_on heatmap ===
plt.figure(figsize=(9, 3))
im = plt.imshow(Von_map.T - V_thre, cmap='plasma', aspect='equal', origin='lower')  # Transpose for XY match
cbar = plt.colorbar(im, shrink=0.75)
cbar.set_label("Vbr (V)")
plt.title(f"2D Breakdown Voltage Map")
plt.xlabel("X pixels")
plt.ylabel("Y pixels")
plt.tight_layout()
plt.show()

# === Plot histogram of breakdown voltages ===
plt.figure(figsize=(7, 4))
valid_vons = Von_map[~np.isnan(Von_map)].flatten()
plt.hist(valid_vons-V_thre, bins=12, color='steelblue', edgecolor='black')
plt.xlabel("Vbr (V)")
plt.ylabel("Number of Pixels")
plt.title("Histogram of Breakdown Voltages (Vbr)")
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()

# === Save Vbr map ===
vbr_map = Von_map - V_thre  # Convert V_on to Vbr by subtracting threshold
save_path = os.path.join(folder, "vbr_map.npy")
np.save(save_path, vbr_map)
print(f"[INFO] Vbr map saved to {save_path}")
