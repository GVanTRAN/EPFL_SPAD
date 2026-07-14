import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import loadmat
import re
from matplotlib.colors import LogNorm

# === CONFIG ===
folder_before = r'C:/Users/Admin/OneDrive - epfl.ch/Desktop/kerim analysis/2508/chip4_AI_#1'
folder_after  = r'C:/Users/Admin/OneDrive - epfl.ch/Desktop/kerim analysis/2808/chip4_AI_AA_#2'
pixel_area = 19.63  # µm²
frame_rate = 1.66e3  # counts/s

# === DCR Loader ===
def get_dcr_files(folder):
    volt_dict = {}
    for fname in os.listdir(folder):
        if fname.startswith("DCR") and fname.endswith(".mat"):
            m = re.search(r"DCR_\d+_(\d{2,3}(?:\.\d+)?)_\d+\.mat", fname)
            if m:
                v = float(m.group(1))
                volt_dict[v] = os.path.join(folder, fname)
    return volt_dict

def load_dcr(file_path):
    mat = loadmat(file_path)
    varname = [k for k in mat if not k.startswith("__")][0]
    dcr = np.nan_to_num(mat[varname]) / pixel_area
    return dcr

# === Get all matching voltages ===
before_files = get_dcr_files(folder_before)
after_files = get_dcr_files(folder_after)
common_voltages = sorted(set(before_files.keys()) & set(after_files.keys()))

# === Plot each voltage ===
for v in common_voltages:
    dcr_before = load_dcr(before_files[v])
    dcr_after  = load_dcr(after_files[v])

    flat_before = dcr_before.flatten()
    flat_after  = dcr_after.flatten()


    # === Plot ===
    plt.figure(figsize=(8, 6))
    plt.scatter(flat_before, flat_after, s=10, alpha=0.4, label="Pixels")

    # y = x line
    min_val = min(flat_before.min(), flat_after.min())
    max_val = max(flat_before.max(), flat_after.max())
    plt.plot([min_val, max_val], [min_val, max_val], '--', color='black', label='y = x')

    # Frame rate
    plt.axhline(frame_rate, color='red', linestyle='--', label='Frame Rate')
    plt.axvline(frame_rate, color='red', linestyle='--')

    # Median point
    med_x = np.median(flat_before)
    med_y = np.median(flat_after)
    plt.scatter(med_x, med_y, color='blue', s=80, edgecolor='black', zorder=10, label='Median DCR')

    # Labels
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel("DCR Before Annealing (cps/µm²)", fontsize=12)
    plt.ylabel("DCR After Annealing (cps/µm²)", fontsize=12)
    plt.title(f"DCR Scatter @ {v:.2f} V", fontsize=14)
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    #plt.ylim(3e-3, 3e3)
    #plt.xlim(3e-3, 3e3)
    plt.legend()
    plt.tight_layout()
    plt.show()

    # === Delta & Ratio Heatmaps ===
    delta_dcr = np.rot90(dcr_after - dcr_before)
    ratio_dcr = np.rot90(dcr_after / (dcr_before + 1e-5))  # avoid division by zero

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    im1 = ax1.imshow(delta_dcr, cmap='seismic', norm=LogNorm(vmin=1e-2, vmax=np.max(np.abs(delta_dcr))))
    ax1.set_title(f"ΔDCR (After - Before) @ {v:.2f} V")
    plt.colorbar(im1, ax=ax1, fraction=0.046, pad=0.04)

    im2 = ax2.imshow(ratio_dcr, cmap='plasma', norm=LogNorm(vmin=1e-1, vmax=np.max(ratio_dcr)))
    ax2.set_title(f"DCR Ratio (After / Before) @ {v:.2f} V")
    plt.colorbar(im2, ax=ax2, fraction=0.046, pad=0.04)

    plt.suptitle(f"DCR Radiation Effect Maps @ {v:.2f} V", fontsize=16)
    plt.tight_layout()
    plt.show()
