import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import loadmat
import re

# === Config ===
folder = r"C:/Users/Admin/OneDrive - epfl.ch/Desktop/kerim analysis/2708/PDP/chip3_AI_#3"
area = 19.63  # in µm²
target_voltage = 22.0

# === Storage ===
lcr_curves = {}
net_curves = {}
dcr_sorted = None

# === Load LCRs and match with same-voltage DCRs ===
for fname in os.listdir(folder):
    if fname.startswith('LCR') and fname.endswith('.mat'):
        match = re.search(r'LCR_\d+_(\d{2,3}(?:\.\d+)?)_(\d+?)_(\d+)\.mat', fname)
        if match:
            voltage = float(match.group(1))
            wavelength = int(match.group(2))
            exposure = int(match.group(3))

            if voltage != target_voltage:
                continue

            # Load LCR
            lcr_path = os.path.join(folder, fname)
            lcr_mat = loadmat(lcr_path)
            lcr_var = [k for k in lcr_mat if not k.startswith('__')][0]
            lcr_2d = lcr_mat[lcr_var] 

            # Find matching DCR with same voltage
            dcr_2d = None
            for dname in os.listdir(folder):
                if dname.startswith("DCR") and dname.endswith(".mat"):
                    dmatch = re.search(r'DCR_\d+_(\d{2,3}(?:\.\d+)?)_(\d+)\.mat', dname)
                    if dmatch and np.isclose(float(dmatch.group(1)), voltage):
                        dcr_path = os.path.join(folder, dname)
                        dcr_mat = loadmat(dcr_path)
                        dcr_var = [k for k in dcr_mat if not k.startswith('__')][0]
                        dcr_2d = dcr_mat[dcr_var]
                        break

            if dcr_2d is None:
                print(f"[SKIP] No DCR found for voltage {voltage}")
                continue
            if lcr_2d.shape != dcr_2d.shape:
                print(f"[SKIP] Shape mismatch in {fname}")
                continue

            # Sort and store
            label = f"{wavelength} nm"
            raw_sorted = np.sort(lcr_2d[~np.isnan(lcr_2d)])
            lcr_curves[label] = raw_sorted

            net = lcr_2d - dcr_2d
            #net[net < 0] = 0
            net_sorted = np.sort(net[~np.isnan(net)])
            net_curves[label] = net_sorted

            # Save one dcr_sorted for reference plot (can be overwritten)
            dcr_sorted = np.sort(dcr_2d[~np.isnan(dcr_2d)])


# === Plot ===
fig, axs = plt.subplots(1, 2, figsize=(12, 5))  # No sharey

# --- Left: LCR + DCR ---
for label, sorted_vals in lcr_curves.items():
    percent = np.linspace(0, 100, len(sorted_vals))
    axs[0].plot(percent, sorted_vals, label=label)
axs[0].plot(np.linspace(0, 100, len(dcr_sorted)), dcr_sorted, 'k--', label='DCR', linewidth=2)

axs[0].set_title("Cumulative LCR, DCR")
axs[0].set_xlabel("Cumulative % of Pixels")
axs[0].set_ylabel("Count Rate (cps)")
axs[0].set_yscale("log")
#axs[0].set_xlim(95,102)
#axs[0].set_ylim(1e2,2e3)
axs[0].grid(True, which="both")
axs[0].legend(title="Wavelength")

# --- Right: Net (LCR - DCR) ---
for label, sorted_vals in net_curves.items():
    percent = np.linspace(0, 100, len(sorted_vals))
    axs[1].plot(percent, sorted_vals, label=label)
#axs[1].plot(np.linspace(0, 100, len(dcr_sorted)), dcr_sorted, 'k--', label='DCR', linewidth=2)

axs[1].set_title("Cumulative (LCR - DCR)")
axs[1].set_xlabel("Cumulative % of Pixels")
axs[1].set_ylabel("Net Count Rate (cps)")
#axs[1].set_xlim(95,102)
#axs[1].set_ylim(-0.1,20)
#axs[1].set_ylim(-0.1,100)
axs[1].set_yscale("log")
axs[1].grid(True, which="both")
axs[1].legend(title="Wavelength")

plt.suptitle(f"Cumulative DCR and Net Signal at {target_voltage} V (log scale)")
plt.tight_layout()
plt.show()
