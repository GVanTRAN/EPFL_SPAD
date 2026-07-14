import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import loadmat
import re

# === Config: Paths ===
folder_0907_chip0 = r'C:/Users/Admin/OneDrive - epfl.ch/Desktop/kerim analysis/0907'

folder_1407 = r'C:/Users/Admin/OneDrive - epfl.ch/Desktop/kerim analysis/1407'
folder_1507 = r'C:/Users/Admin/OneDrive - epfl.ch/Desktop/kerim analysis/1507'
folder_1507s = r'C:/Users/Admin/OneDrive - epfl.ch/Desktop/kerim analysis/1507suite'
folder_1507ss = r'C:/Users/Admin/OneDrive - epfl.ch/Desktop/kerim analysis/1507suitesuite'
folder_1607 = r'C:/Users/Admin/OneDrive - epfl.ch/Desktop/kerim analysis/1607/chip1'

folder_1607_chip2_1 = r'C:/Users/Admin/OneDrive - epfl.ch/Desktop/kerim analysis/1607/chip2_#1'

folder_1707_chip3_1 = r'C:/Users/Admin/OneDrive - epfl.ch/Desktop/kerim analysis/1707/chip3_#1'
folder_1707_chip3_2 = r'C:/Users/Admin/OneDrive - epfl.ch/Desktop/kerim analysis/1707/chip3_#2'
folder_1807_chip3_3 = r'C:/Users/Admin/OneDrive - epfl.ch/Desktop/kerim analysis/1807/chip3_#3'
folder_1807_chip3_4 = r'C:/Users/Admin/OneDrive - epfl.ch/Desktop/kerim analysis/1807/chip3_#4'
folder_1807_chip3_5 = r'C:/Users/Admin/OneDrive - epfl.ch/Desktop/kerim analysis/1807/chip3_#5'

folder_1807_chip4_1 = r'C:/Users/Admin/OneDrive - epfl.ch/Desktop/kerim analysis/1807/chip4_#1'
folder_1807_chip4_2 = r'C:/Users/Admin/OneDrive - epfl.ch/Desktop/kerim analysis/1807/chip4_#2'

folder_2207_chip5_1 = r'C:/Users/Admin/OneDrive - epfl.ch/Desktop/kerim analysis/2207/chip5_#1'
folder_2207_chip5_2 = r'C:/Users/Admin/OneDrive - epfl.ch/Desktop/kerim analysis/2207/chip5_#2'
folder_2207_chip5_3 = r'C:/Users/Admin/OneDrive - epfl.ch/Desktop/kerim analysis/2207/chip5_#3'

folder_2207_chip6_1 = r'C:/Users/Admin/OneDrive - epfl.ch/Desktop/kerim analysis/2207/chip6_#1'
folder_2207_chip6_2 = r'C:/Users/Admin/OneDrive - epfl.ch/Desktop/kerim analysis/2207/chip6_#2'

folder_2807_chip7_1 = r'C:/Users/Admin/OneDrive - epfl.ch/Desktop/kerim analysis/2807/chip7_#1'
folder_2807_chip7_2 = r'C:/Users/Admin/OneDrive - epfl.ch/Desktop/kerim analysis/2807/chip7_#2'
folder_2807_chip7_3 = r'C:/Users/Admin/OneDrive - epfl.ch/Desktop/kerim analysis/2807/chip7_#3'
folder_2807_chip7_4 = r'C:/Users/Admin/OneDrive - epfl.ch/Desktop/kerim analysis/2807/chip7_#4'
folder_2807_chip7_5 = r'C:/Users/Admin/OneDrive - epfl.ch/Desktop/kerim analysis/2807/chip7_#5'

folder_3007_chip8_1 = r'C:/Users/Admin/OneDrive - epfl.ch/Desktop/kerim analysis/3007/chip8_#1'
folder_3007_chip8_2 = r'C:/Users/Admin/OneDrive - epfl.ch/Desktop/kerim analysis/3007/chip8_#2'
folder_3007_chip8_3 = r'C:/Users/Admin/OneDrive - epfl.ch/Desktop/kerim analysis/3007/chip8_#3'
folder_3007_chip8_4 = r'C:/Users/Admin/OneDrive - epfl.ch/Desktop/kerim analysis/3007/chip8_#4'
folder_3007_chip8_5 = r'C:/Users/Admin/OneDrive - epfl.ch/Desktop/kerim analysis/3007/chip8_#5'

folder_0508_chip7_20_1 = r'C:/Users/Admin/OneDrive - epfl.ch/Desktop/kerim analysis/0508/chip7/T20'

folder_0508_chip8_20_1 = r'C:/Users/Admin/OneDrive - epfl.ch/Desktop/kerim analysis/0508/chip8/T20/DCR/#1'
folder_0508_chip8_20_2 = r'C:/Users/Admin/OneDrive - epfl.ch/Desktop/kerim analysis/0508/chip8/T20/DCR/#2'

area = 19.63  # in µm²

# --- single spad ---1507 1 
ovs1_1 = np.array([20.5, 20.75, 21, 21.25, 21.5, 21.75, 22, 22.25, 22.5, 22.75, 23, 23.25, 23.5])
oms1_1 = np.array([19.4, 65.2, 86, 149, 189.2,246.2, 304,354, 410.6, 486.625, 556.86, 686.71, 59534158.25])/30


# --- single spad ---1507 2 
ovs1_2 = np.array([20.5, 21, 21.5, 22, 22.5,23])
oms1_2 = np.array([26.6, 96.2, 147.4, 228.25, 258285.3, 458349])/30

# --- single spad ---1507 3
ovs1_3 = np.array([20.5, 21, 21.5, 22, 22.5, 23, 23.25])
oms1_3 = np.array([0, 162, 268.3, 409, 541, 1232, 93210])/30

# --- single spad ---1507 4
ovs1_4 = np.array([20.5, 21, 21.5, 22, 22.5,23, 23.25])
oms1_4 = np.array([26.5, 85, 159, 234, 336, 3270, 75000])/30

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

# === Previous data ===Kerim
ov = np.array([21.5, 22, 22.5, 23, 23.2]) # 23.2
om = np.array([1.74, 2.63, 6.65, 113.1, 799.6]) # 799.6

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

# === Load both datasets ===
v_0907_0, med_0907 = load_median_dcr(folder_0907_chip0)

v_1407, med_1407 = load_median_dcr(folder_1407)
v_1507, med_1507 = load_median_dcr(folder_1507)
v_1507s, med_1507s = load_median_dcr(folder_1507s)
v_1507ss, med_1507ss = load_median_dcr(folder_1507ss)
v_1607, med_1607 = load_median_dcr(folder_1607)

v_1607_2_1, med_1607_2_1 = load_median_dcr(folder_1607_chip2_1)

v_1707_3_1, med_1707_3_1 = load_median_dcr(folder_1707_chip3_1)
v_1707_3_2, med_1707_3_2 = load_median_dcr(folder_1707_chip3_2)
v_1807_3_3, med_1807_3_3 = load_median_dcr(folder_1807_chip3_3)
v_1807_3_4, med_1807_3_4 = load_median_dcr(folder_1807_chip3_4)
v_1807_3_5, med_1807_3_5 = load_median_dcr(folder_1807_chip3_5)

v_1807_4_1, med_1807_4_1 = load_median_dcr(folder_1807_chip4_1)
v_1807_4_2, med_1807_4_2 = load_median_dcr(folder_1807_chip4_2)

v_2207_5_1, med_2207_5_1 = load_median_dcr(folder_2207_chip5_1)
v_2207_5_2, med_2207_5_2 = load_median_dcr(folder_2207_chip5_2)
v_2207_5_3, med_2207_5_3 = load_median_dcr(folder_2207_chip5_3)

v_2207_6_1, med_2207_6_1 = load_median_dcr(folder_2207_chip6_1)
v_2207_6_2, med_2207_6_2 = load_median_dcr(folder_2207_chip6_2)

v_2807_7_1, med_2807_7_1 = load_median_dcr(folder_2807_chip7_1)
v_2807_7_2, med_2807_7_2 = load_median_dcr(folder_2807_chip7_2)
v_2807_7_3, med_2807_7_3 = load_median_dcr(folder_2807_chip7_3)
v_2807_7_4, med_2807_7_4 = load_median_dcr(folder_2807_chip7_4)
v_2807_7_5, med_2807_7_5 = load_median_dcr(folder_2807_chip7_5)

v_3007_8_1, med_3007_8_1 = load_median_dcr(folder_3007_chip8_1)
v_3007_8_2, med_3007_8_2 = load_median_dcr(folder_3007_chip8_2)
v_3007_8_3, med_3007_8_3 = load_median_dcr(folder_3007_chip8_3)
v_3007_8_4, med_3007_8_4 = load_median_dcr(folder_3007_chip8_4)
v_3007_8_5, med_3007_8_5 = load_median_dcr(folder_3007_chip8_5)

v_0508_7_20_1, med_508_7_20_1 = load_median_dcr(folder_0508_chip7_20_1)

v_0508_8_20_1, med_508_8_20_1 = load_median_dcr(folder_0508_chip8_20_1)
v_0508_8_20_2, med_508_8_20_2 = load_median_dcr(folder_0508_chip8_20_2)

# === Plot: Log Scale Only ===
plt.figure(figsize=(8, 6))

plt.plot(ov, om / area, marker='x', linestyle='--', label='Old Data (Kerim)', c = 'orange')

### chip 0 ###
#plt.plot(v_0907_0, med_0907 / area, marker='v', label='Chip 0 #1')

#plt.plot(v_1407, med_1407 / area, marker='o', label='Median Chip 1')
#plt.plot(v_1507, med_1507 / area, marker='v', label='Chip 1 #1', c = 'r')
#plt.plot(ovs1_1, oms1_1 / area , marker='x', linestyle='--', label='sSPAD 1 #1')
#plt.plot(v_1507s, med_1507s / area, marker='v', label='Chip 1 #2')
#plt.plot(ovs1_2, oms1_2 /area , marker='x', linestyle='--', label='sSPAD 1 #2',  c = 'b')
#plt.plot(v_1507ss, med_1507ss / area, marker='v', label='Median Chip 1 #3')
#plt.plot(ovs1_3, oms1_3 /area , marker='x', linestyle='--', label='sSPAD 1 #3')
#plt.plot(v_1607, med_1607 / area, marker='v', label='Chip 1 #4')
#plt.plot(ovs1_4, oms1_4 /area , marker='x', linestyle='--', label='sSPAD 1 #4')


#### chip2 ###
#plt.plot(v_1607_2_1, med_1607_2_1 / area, marker='v', label='Chip 2 #1')
#plt.plot(ovs2_1, oms2_1 / area, marker='v', linestyle='--', label='single spad 2 #1')

### chip3 ###
#plt.plot(v_1707_3_1, med_1707_3_1 / area, marker='v', label='Chip 3 #1')
#plt.plot(ovs3_1, oms3_1 / area, marker='o', label = 'sSPAD c3 #1')
#plt.plot(v_1707_3_2, med_1707_3_2 / area, marker='v', label='Chip 3 #2')
#plt.plot(ovs3_2, oms3_2 / area, label = 'sSPAD c3 #2')
#plt.plot(v_1807_3_3, med_1807_3_3 / area, marker='v', label='Chip 3 #3')
#plt.plot(ovs3_3, oms3_3 / area, label = 'sSPAD c3 #3')
#plt.plot(v_1807_3_4, med_1807_3_4 / area, marker='v', label='Chip 3 #4')
#plt.plot(ovs3_4, oms3_4 / area, label = 'sSPAD c3 #4')
#plt.plot(v_1807_3_5, med_1807_3_5 / area, marker='v', label='Chip 3 #5')
#plt.plot(ovs3_5, oms3_5 / area, marker='o', label = 'sSPAD c3 #5')

### chip4 ###
#plt.plot(v_1807_4_1, med_1807_4_1 / area, marker='v', label='Chip 4')
#plt.plot(ovs4_1, oms4_1 / area, marker='v', label='sSPAD 4 #1')
#plt.plot(v_1807_4_2, med_1807_4_2 / area, marker='v', label='Chip 4 #2')
#plt.plot(ovs4_2, oms4_2 / area, marker='v', label='sSPAD 4 #2')

### chip 5 ### 
#plt.plot(v_2207_5_1, med_2207_5_1 / area, marker='v', label='Chip 5 #1')
#plt.plot(v_2207_5_2, med_2207_5_2 / area, marker='v', label='Chip 5 #2')
#plt.plot(v_2207_5_3, med_2207_5_3 / area, marker='v', label='Chip 5 #3')

### chip 6 ### 
#plt.plot(v_2207_6_1, med_2207_6_1 / area, marker='v', label='Chip 6 #1')

### chip 7 ### 
#plt.plot(v_2807_7_1, med_2807_7_1 / area, marker='v', label='Chip 7 #1')
#plt.plot(v_2807_7_2, med_2807_7_2 / area, marker='v', label='Chip 7 #2')
#plt.plot(v_2807_7_3, med_2807_7_3 / area, marker='v', label='Chip 7 #3')
#plt.plot(v_2807_7_4, med_2807_7_4 / area, marker='v', label='Chip 7 #4')
plt.plot(v_2807_7_5, med_2807_7_5 / area, marker='v', label='Chip 7 #5')

### chip 8 ### 
#plt.plot(v_3007_8_1, med_3007_8_1 / area, marker='v', label='Chip 8 #1')
#plt.plot(v_3007_8_2, med_3007_8_2 / area, marker='v', label='Chip 8 #2')
#plt.plot(v_3007_8_3, med_3007_8_3 / area, marker='v', label='Chip 8 #3')
#plt.plot(v_3007_8_4, med_3007_8_4 / area, marker='v', label='Chip 8 #4')
#plt.plot(v_3007_8_5, med_3007_8_5 / area, marker='v', label='Chip 8 #5')

plt.plot(v_0508_7_20_1, med_508_7_20_1 /area , marker='v', label='Chip 7 T20 #1')

#plt.plot(v_0508_8_20_1, med_508_8_20_1 /area , marker='v', label='Chip 8 T20 #1')
#plt.plot(v_0508_8_20_2, med_508_8_20_2 /area , marker='v', label='Chip 8 T20 #2')

### PLOT CONFIG ### 
plt.yscale('log')
plt.title('DCR vs Bias Voltage (Log Scale)')
plt.xlabel('Bias Voltage (V)')
plt.ylabel('normalized DCR (cps/μm²)')
plt.grid(True, which='both')
plt.xlim(20.5, 23.75)
#plt.ylim(-0.1,2)
plt.legend()
plt.tight_layout()
plt.show()
