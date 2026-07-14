import numpy as np
import pandas as pd
from scipy.io import loadmat

def get_incident_photons(mat_file_path, calib_file_path, spad_area_um2=19.63, spot_area_m2=0.0001):
    h = 6.626e-34  # Planck's constant (J·s)
    c = 299792458  # Speed of light (m/s)

    spad_area_m2 = spad_area_um2 * 1e-12

    # === Load .mat file ===
    mat = loadmat(mat_file_path)
    ref_current = np.abs(mat['RefCurrent'])  # ensure all current values are positive
    wavelengths = np.abs(mat['wavelength'].flatten())  # ensure positive wavelengths
    avg_current = np.mean(ref_current, axis=1)

    # === Load calibration responsivity ===
    calib = pd.read_excel(calib_file_path, header=None, names=['Wavelength', 'Responsivity'])
    calib['Wavelength'] = np.abs(calib['Wavelength'])  # clean wavelength data
    calib['Responsivity'] = np.abs(calib['Responsivity'])  # ensure positive responsivity

    photon_flux = []
    for wl, current in zip(wavelengths, avg_current):
        match = calib.loc[np.isclose(calib['Wavelength'], wl, atol=1e-2)]
        if not match.empty:
            resp = match['Responsivity'].values[0]
            power = abs(current) / abs(resp)  # ensure positivity
            irradiance = power / spot_area_m2
            power_spad = irradiance * spad_area_m2
            flux = power_spad * wl * 1e-9 / (h * c)
        else:
            flux = np.nan
        photon_flux.append(flux)

    return np.array(wavelengths), np.array(photon_flux)
