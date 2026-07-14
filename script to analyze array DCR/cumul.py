import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import loadmat
import re

# --- Folder containing your .mat files ---
folder_path = r'C:/Users/Admin/OneDrive - epfl.ch/Desktop/kerim analysis/2508/chip6_AI_#1'  # ← change this to your actual path
area = 19.63  # in um²
# --- Plot setup ---
plt.figure(figsize=(8, 6))

# --- Loop through .mat files ---
for fname in os.listdir(folder_path):
    if fname.endswith('.mat'):
        path = os.path.join(folder_path, fname)
        try:
            mat = loadmat(path)
            # Get variable (ignore __header__, etc.)
            varname = [k for k in mat.keys() if not k.startswith('__')][0]
            cps = mat[varname].flatten()
            cps = cps[~np.isnan(cps)]
            cps_sorted = np.sort(cps)/area
            percent = np.linspace(0, 100, len(cps_sorted))

            # Extract number from filename using regex
            match = re.search(r'DCR.*?_(\d{2,3}(?:\.\d+)?)_', fname)
            label = match.group(1) if match else fname

            plt.plot(percent, cps_sorted, label=label)
        except Exception as e:
            print(f"Error with {fname}: {e}")

# --- Final plot setup ---
plt.xlabel('Cumulative %')
plt.ylabel('DCR (cps/μm²)')
plt.yscale("log")
#plt.ylim(0,1e1)
plt.title('cdf - normalized DCR Plot')

# Get handles and labels from current figure
handles, labels = plt.gca().get_legend_handles_labels()

# Sort legend entries numerically
sorted_pairs = sorted(zip(labels, handles), key=lambda x: float(x[0]))
sorted_labels, sorted_handles = zip(*sorted_pairs)

# Display sorted legend
plt.legend(sorted_handles, sorted_labels, title='bias voltage (V)', fontsize='small')

plt.grid(True)
plt.tight_layout()
plt.show()
