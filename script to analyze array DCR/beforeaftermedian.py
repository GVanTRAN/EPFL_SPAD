import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import loadmat
import re

# === Config: Paths ===

folder_1607_chip1_BI = r'C:/Users/Admin/OneDrive - epfl.ch/Desktop/kerim analysis/1607/chip1'
folder_2508_chip1_AI_1 = r'C:/Users/Admin/OneDrive - epfl.ch/Desktop/kerim analysis/2508/chip1_AI_#1'
folder_2508_chip1_AI_2 = r'C:/Users/Admin/OneDrive - epfl.ch/Desktop/kerim analysis/2508/chip1_AI_#2'
folder_2808_chip1_AI_3 = r'C:/Users/Admin/OneDrive - epfl.ch/Desktop/kerim analysis/2808/chip1_AI_#3'
folder_2908_chip1_AI_AA_1 = r'C:/Users/Admin/OneDrive - epfl.ch/Desktop/kerim analysis/2908/chip1_AI_AA_#1'

folder_1807_chip3_5 = r'C:/Users/Admin/OneDrive - epfl.ch/Desktop/kerim analysis/1807/chip3_#5'
folder_2508_chip3_AI_1 = r'C:/Users/Admin/OneDrive - epfl.ch/Desktop/kerim analysis/2508/chip3_AI_#1'
folder_2808_chip3_AI_4 = r'C:/Users/Admin/OneDrive - epfl.ch/Desktop/kerim analysis/2808/chip3_AI_#4'


folder_1807_chip4_2 = r'C:/Users/Admin/OneDrive - epfl.ch/Desktop/kerim analysis/1807/chip4_#2'
folder_2508_chip4_AI_1 = r'C:/Users/Admin/OneDrive - epfl.ch/Desktop/kerim analysis/2508/chip4_AI_#1'
folder_2708_chip4_AI_AA_1 = r'C:/Users/Admin/OneDrive - epfl.ch/Desktop/kerim analysis/2708/chip4_AI_AA_#1'
folder_2808_chip4_AI_AA_2 = r'C:/Users/Admin/OneDrive - epfl.ch/Desktop/kerim analysis/2808/chip4_AI_AA_#2'

folder_2207_chip5_3 = r'C:/Users/Admin/OneDrive - epfl.ch/Desktop/kerim analysis/2207/chip5_#3'
folder_2508_chip5_AI_1 = r'C:/Users/Admin/OneDrive - epfl.ch/Desktop/kerim analysis/2508/chip5_AI_#1'
folder_2808_chip5_AI_2 = r'C:/Users/Admin/OneDrive - epfl.ch/Desktop/kerim analysis/2808/chip5_AI_#2'
folder_2808_chip5_AI_AA_1 = r'C:/Users/Admin/OneDrive - epfl.ch/Desktop/kerim analysis/2808/chip5_AI_AA_#1'

folder_2207_chip6_1 = r'C:/Users/Admin/OneDrive - epfl.ch/Desktop/kerim analysis/2207/chip6_#1'
folder_2508_chip6_AI_1 = r'C:/Users/Admin/OneDrive - epfl.ch/Desktop/kerim analysis/2508/chip6_AI_#1'
folder_2708_chip6_AI_AA_1 = r'C:/Users/Admin/OneDrive - epfl.ch/Desktop/kerim analysis/2708/chip6_AI_AA_#1'
folder_2908_chip6_AI_AA_2 = r'C:/Users/Admin/OneDrive - epfl.ch/Desktop/kerim analysis/2908/chip6_AI_AA_#2'

area = 19.63  # in µm²

# === Function to load voltages and medians from folder ===
def load_median_dcr(folder_path):
    voltages = []
    medians = []
    for fname in os.listdir(folder_path):
        if fname.endswith('.mat'):
            try:
                mat = loadmat(os.path.join(folder_path, fname))
                varname = [k for k in mat.keys() if not k.startswith('__')][0]
                cps = mat[varname].flatten()
                cps = cps[~np.isnan(cps)]
                match = re.search(r'DCR.*?_(\d{2,3}(?:\.\d+)?)_', fname)
                if match:
                    voltage = float(match.group(1))
                    voltages.append(voltage)
                    medians.append(np.median(cps))
                else:
                    print(f"[WARN] No voltage found in: {fname}")
            except Exception as e:
                print(f"[ERROR] {fname}: {e}")
    voltages = np.array(voltages)
    medians = np.array(medians)
    sort_idx = np.argsort(voltages)
    return voltages[sort_idx], medians[sort_idx]

### === LOAD FILES === ### 

    ### chip 1 ### 
v_1607, med_1607 = load_median_dcr(folder_1607_chip1_BI)
v_2508_chip1_AI_1, med_2508_chip1_AI_1 = load_median_dcr(folder_2508_chip1_AI_1)
v_2508_chip1_AI_2, med_2508_chip1_AI_2 = load_median_dcr(folder_2508_chip1_AI_2)
v_2808_chip1_AI_3, med_2808_chip1_AI_3 = load_median_dcr(folder_2808_chip1_AI_3)
v_2908_chip1_AI_AA_1, med_2908_chip1_AI_AA_1 = load_median_dcr(folder_2908_chip1_AI_AA_1)

    ### chip 3 ###
v_1807_3_5, med_1807_3_5 = load_median_dcr(folder_1807_chip3_5)
v_2508_chip3_AI_1, med_2508_chip3_AI_1 = load_median_dcr(folder_2508_chip3_AI_1)
v_2808_chip3_AI_4, med_2808_chip3_AI_4 = load_median_dcr(folder_2808_chip3_AI_4)


    ### chip 4 ###
v_1807_4_2, med_1807_4_2 = load_median_dcr(folder_1807_chip4_2)
v_2508_chip4_AI_1, med_2508_chip4_AI_1 = load_median_dcr(folder_2508_chip4_AI_1)
v_2708_chip4_AI_AA_1, med_2708_chip4_AI_AA_1 = load_median_dcr(folder_2708_chip4_AI_AA_1)
v_2808_chip4_AI_AA_2, med_2808_chip4_AI_AA_2 = load_median_dcr(folder_2808_chip4_AI_AA_2)

    ### chip 5 ###
v_2207_5_3, med_2207_5_3 = load_median_dcr(folder_2207_chip5_3)
v_2508_chip5_AI_1, med_2508_chip5_AI_1 = load_median_dcr(folder_2508_chip5_AI_1)
v_2808_chip5_AI_2, med_2808_chip5_AI_2 = load_median_dcr(folder_2808_chip5_AI_2)
v_2808_chip5_AI_AA_1, med_2808_chip5_AI_AA_1 = load_median_dcr(folder_2808_chip5_AI_AA_1)

    ### chip 6 ###
v_2207_6_1, med_2207_6_1 = load_median_dcr(folder_2207_chip6_1)
v_2508_chip6_AI_1, med_2508_chip6_AI_1 = load_median_dcr(folder_2508_chip6_AI_1)
v_2708_chip6_AI_AA_1, med_2708_chip6_AI_AA_1 = load_median_dcr(folder_2708_chip6_AI_AA_1)
v_2908_chip6_AI_AA_2, med_2908_chip6_AI_AA_2 = load_median_dcr(folder_2908_chip6_AI_AA_2)


# === Plot: Log Scale Only ===
plt.figure(figsize=(8, 6))
#plt.plot(v_2207_6_1, med_2207_6_1 / area, marker = 'v', label = 'BI')

v1 = np.array([20.75, 21, 21.25, 21.5, 21.75, 22, 22.5, 23])
c1 = np.array([8059,12101, 16722, 20518, 25404, 32660, 46941, 65040]) / (10 * area)

#plt.plot(v_1607, med_1607 / area, marker='v', label='Chip 1 BI')
#plt.plot(v_2508_chip1_AI_1, med_2508_chip1_AI_1 / area, marker = 'v', label = 'Chip 1 AI: 1e12 #1')
#plt.plot(v_2508_chip1_AI_2, med_2508_chip1_AI_2 / area, marker = 'v', label = 'Chip 1 AI #2')
#plt.plot(v_2808_chip1_AI_3, med_2808_chip1_AI_3 / area, marker = 'v', label = 'Chip 1 AI: 1e12 #3')
#plt.plot(v_2908_chip1_AI_AA_1, med_2908_chip1_AI_AA_1 / area, marker = 'v', label = 'Chip 1 AI: 1e12 AA #1')
#plt.plot(v1,c1, label = 'single spad 1', marker='v')

v3 = np.array([20.75, 21, 21.25, 21.5, 22, 22.25, 22.5, 22.75, 23])
c3 = np.array([123, 141, 214, 302, 362, 443, 533, 680, 712]) / (10 * area)
#plt.plot(v_1807_3_5, med_1807_3_5 / area, marker = 'v', label = 'Chip 3 BI')
#plt.plot(v_2508_chip3_AI_1, med_2508_chip3_AI_1 / area, marker = 'v', label = 'Chip 3 AI: 1e11')
#plt.plot(v_2808_chip3_AI_4, med_2808_chip3_AI_4 / area, marker = 'v', label = 'Chip 3 AI: 1e11 #4')
#plt.plot(v3,c3, label = 'single spad 3', marker='v')

plt.plot(v_1807_4_2, med_1807_4_2 / area, marker = 'v', label = 'Chip 4 BI')
plt.plot(v_2508_chip4_AI_1, med_2508_chip4_AI_1 / area, marker = 'v', label = 'Chip 4 AI: 1e13')
plt.plot(v_2708_chip4_AI_AA_1, med_2708_chip4_AI_AA_1 / area, marker = 'v', label = 'Chip 4 AI: 1e13 AA #1')
plt.plot(v_2808_chip4_AI_AA_2, med_2808_chip4_AI_AA_2 / area, marker = 'v', label = 'Chip 4 AI: 1e13 AA #2')

v2 = np.array([20.75, 21, 21.5, 22, 22.5, 23])
c2 = np.array([90, 1749, 4293, 9168, 18144, 28361994]) / (10 * area)
#plt.plot(v_2207_5_3, med_2207_5_3 / area, marker = 'v', label = 'Chip 5 BI')
#plt.plot(v_2508_chip5_AI_1, med_2508_chip5_AI_1 / area, marker = 'v', label = 'Chip 5 AI: 1e12 #1')
#plt.plot(v_2808_chip5_AI_2, med_2808_chip5_AI_2 / area, marker = 'v', label = 'Chip 5 AI: 1e12 #2')
#plt.plot(v_2808_chip5_AI_AA_1, med_2808_chip5_AI_AA_1 / area, marker = 'v', label = 'Chip 5 AI: 1e12 AA #1')
#plt.plot(v2,c2, label = 'single spad 5', marker='v')

#plt.plot(v_2207_6_1, med_2207_6_1 / area, marker = 'v', label = 'Chip 6 BI')
#plt.plot(v_2508_chip6_AI_1, med_2508_chip6_AI_1 / area, marker = 'v', label = 'Chip 6 AI: 1e13')
#plt.plot(v_2708_chip6_AI_AA_1, med_2708_chip6_AI_AA_1 / area, marker = 'v', label = 'Chip 6 AI: 1e13 AA #1')
#plt.plot(v_2908_chip6_AI_AA_2, med_2908_chip6_AI_AA_2 / area, marker = 'v', label = 'Chip 6 AI: 1e13 AA #2')

plt.axhline(1.66e3, label = 'Frame Rate', color = 'red', linestyle = '--')
plt.xticks(fontsize=12); plt.yticks(fontsize=12)
plt.yscale('log')
plt.title('Median DCR vs Bias Voltage', fontsize = 14)
plt.xlabel('Bias Voltage (V)', fontsize = 14)
plt.ylabel('Normalized DCR (cps/μm²)', fontsize = 14)
plt.grid(True, which='both')
plt.xlim(20.5, 23.75)
#plt.ylim(1e1, 3e3)
#plt.legend(fontsize = 12)
plt.tight_layout()
plt.show()