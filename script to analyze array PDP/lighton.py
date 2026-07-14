# lighton.py
import os
import numpy as np
from scipy.io import loadmat
import re

def get_spad_counts(folder, voltage=22.0, exposure=1500, area=19.63):
    wavelengths = []
    photon_counts = []
    dcr_median = None

    for fname in os.listdir(folder):
        if fname.startswith('DCR') and fname.endswith('.mat'):
            match = re.search(r'DCR_\d+_(\d{2,3}(?:\.\d+)?)_(\d+)\.mat', fname)
            if match and float(match.group(1)) == voltage and int(match.group(2)) == exposure:
                mat = loadmat(os.path.join(folder, fname))
                varname = [k for k in mat if not k.startswith('__')][0]
                cps = mat[varname].flatten()
                cps = cps[~np.isnan(cps)]
                dcr_median = np.median(cps)

    for fname in os.listdir(folder):
        if fname.startswith('LCR') and fname.endswith('.mat'):
            match = re.search(r'LCR_\d+_(\d{2,3}(?:\.\d+)?)_(\d+?)_(\d+)\.mat', fname)
            if match:
                voltage_match = float(match.group(1))
                wavelength = int(match.group(2))
                exposure_match = int(match.group(3))
                if voltage_match == voltage:
                    mat = loadmat(os.path.join(folder, fname))
                    varname = [k for k in mat if not k.startswith('__')][0]
                    cps = mat[varname].flatten()
                    cps = cps[~np.isnan(cps)]
                    median_cps = np.median(cps)
                    wavelengths.append(wavelength)
                    photon_counts.append(median_cps / area)

    wavelengths = np.array(wavelengths)
    photon_counts = np.array(photon_counts)
    sorted_idx = np.argsort(wavelengths)
    return wavelengths[sorted_idx], photon_counts[sorted_idx] * area, dcr_median
