import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import loadmat
import re

# --- Folder containing your .mat files ---
folder_path = r'C:/Users/Admin/OneDrive - epfl.ch/Desktop/kerim analysis/3007/chip8_#1'

# --- Store voltages and medians ---
voltages = []
medians = []
means = []
area = 19.63  # in um²

# --- single spad ---1507
#ovs = np.array([20.5, 20.75, 21, 21.25, 21.5, 21.75, 22, 22.25, 22.5, 22.75, 23, 23.25, 23.5])
#oms = np.array([19.4, 65.2, 86, 149, 189.2,246.2, 304,354, 410.6, 486.625, 556.86, 686.71, 59534158.25])/


# --- single spad ---1507suite
#ovs = np.array([20.5, 21, 21.5, 22, 22.5,23])
#oms = np.array([26.6, 96.2, 147.4, 228.25, 258285.3, 458349])/30

# --- single spad ---1507suitesuite
#ovs = np.array([20.5, 21, 21.5, 22, 22.5,23])
#oms = np.array([0, 161.6, 267, 408.6, 541, 1232])/30

# --- single spad 2---1607
ovs2_1 = np.array([20.5, 20.75, 21, 21.25, 21.5, 21.75, 22, 22.25, 22.5, 22.75, 23])
oms2_1 = np.array([8, 52.625, 110.9, 158.7, 202.9, 255.4, 324.25, 386.5, 426.625, 494.71, 559.375])/30

# --- single spad ---1807 chip 3 #1
ovs3_1 = np.array([20.5, 21, 21.5, 22, 22.5,23])
oms3_1 = np.array([0, 26.875, 57.75, 114, 187, 279.625])/30

# --- single spad ---1807 chip 3 #2
ovs3_2 = np.array([20.5, 21, 21.5, 22, 22.5,23])
oms3_2 = np.array([0, 12.25, 93, 155.875, 257.75, 362.375])/30

# --- single spad ---1807 chip 3 #3
ovs3_3 = np.array([20.5, 21, 21.5, 22, 22.5,23])
oms3_3 = np.array([0, 25.7, 54.7, 92.4, 148.2, 244.7])/30

# --- single spad ---1807 chip 3 #4
ovs3_4 = np.array([20.5, 21, 21.5, 22, 22.5,23])
oms3_4 = np.array([0, 26.7, 70.7, 121.6, 191.1, 271.1])/30

# --- single spad ---1807 chip 3 #5
ovs3_5 = np.array([20.5, 21, 21.5, 22, 22.5,23])
oms3_5 = np.array([0, 30.6, 62.2, 104, 155.2, 245.2])/30

# --- single spad ---1807 chip 4 #1
ovs4_1 = np.array([20.5, 21, 21.5, 22, 22.5,23])
oms4_1 = np.array([0, 15.3, 28.3, 42.9, 77.4, 132830])/30

# --- single spad ---1807 chip 4 #2
ovs4_2 = np.array([20.5, 21, 21.5, 22, 22.5, 22.75, 23])
oms4_2 = np.array([0, 36.8, 64.5, 95, 179.7, 1857, 77945])/30

# --- Previous data (from Kerim) ---
#ov = np.array([21.5, 22, 22.5, 23, 23.2])
#om = np.array([1.74, 2.63, 6.65, 113.1, 799.6])
ov = np.array([21.5, 22, 22.5, 23])
om = np.array([1.74, 2.63, 6.65, 113.1])

# --- Load and compute ---
for fname in os.listdir(folder_path):
    if fname.endswith('.mat'):
        try:
            mat = loadmat(os.path.join(folder_path, fname))
            # Automatically select the first non-system variable
            varname = [k for k in mat.keys() if not k.startswith('__')][0]
            cps = mat[varname].flatten()
            cps = cps[~np.isnan(cps)]

            # Extract voltage using the format DCR_1_22.5_1500.mat
            match = re.search(r'DCR.*?_(\d{2,3}(?:\.\d+)?)_', fname)
            if match:
                voltage = float(match.group(1))
                voltages.append(voltage)
                medians.append(np.median(cps))
                means.append(np.mean(cps))
            else:
                print(f"[WARN] Could not extract voltage from filename: {fname}")
        except Exception as e:
            print(f"[ERROR] {fname}: {e}")

# --- Sort by voltage ---
voltages = np.array(voltages)
medians = np.array(medians)
means = np.array(means)
sort_idx = np.argsort(voltages)
voltages = voltages[sort_idx]
medians = medians[sort_idx]
means = means[sort_idx]

# --- Plot (Linear + Log) ---
fig, axs = plt.subplots(1, 2, figsize=(12, 5), sharex=True)

# Linear
axs[0].plot(voltages, medians / area, marker='o', label = 'Median Chip 4 #2')
# axs[0].plot(voltages, means / area, marker='o', label = 'mean')
axs[0].plot(ovs4_2, oms4_2 / area, marker='x', label="sSPAD 4 #2")
axs[0].plot(ov, om / area, marker='x', label="Old Data (Kerim)")
axs[0].set_title('Normalized Median DCR vs Bias Voltage (Linear)')
axs[0].set_xlabel('Bias Voltage (V)')
axs[0].set_ylabel('Median DCR (cps/μm²)')
axs[0].set_ylim(0, 5)  # Corrected line
axs[0].grid(True)
axs[0].legend()

# Log
axs[1].plot(voltages, medians / area, marker='o', label="Median Chip 4 #2")
# axs[1].plot(voltages, means / area, marker='o', label="Data mean 0907")
axs[1].plot(ovs4_2, oms4_2 / area, marker='x', label="sSPAD 4 #2")
axs[1].plot(ov, om / area, marker='x', label="Old Data (Kerim)")

axs[1].set_yscale('log')
axs[1].set_title('Normalized Median DCR vs Bias Voltage (Log Scale)')
axs[1].set_xlabel('Bias Voltage (V)')
axs[1].set_ylabel('Effective DCR (cps/μm²)')
axs[1].legend()
axs[1].grid(True, which='both')

plt.tight_layout()
plt.show()