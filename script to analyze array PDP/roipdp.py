import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import loadmat
import re
from photonflux import get_incident_photons
from matplotlib.widgets import RectangleSelector
from matplotlib.widgets import TextBox


# === CONFIG ===
folder = r"C:/Users/Admin/OneDrive - epfl.ch/Desktop/kerim analysis/2307/chip3_test_2"
mat_file = os.path.join(folder, "Cal_Phoenix3_2025_23_07_1940_400_20_500_SMU02_Ch1.mat")
calib_file = r"C:/Users/Admin/OneDrive - epfl.ch/Desktop/kerim analysis/Hamamatsu_Resp_320_5_960.xlsx"

area = 19.63  # µm²
target_voltage = 22.0
target_exposure = 1500
target_wavelength = 440

def coords(i, shape): return (i // shape[1], i % shape[1])

# === Load DCR ===
dcr_2d = None
for fname in os.listdir(folder):
    if fname.startswith("DCR") and fname.endswith(".mat"):
        m = re.search(r"DCR_\d+_(\d{2,3}(?:\.\d+)?)_(\d+)\.mat", fname)
        if m:
            v, t = float(m.group(1)), int(m.group(2))
            if v == target_voltage and t == target_exposure:
                dcr_2d = loadmat(os.path.join(folder, fname))
                dcr_2d = dcr_2d[[k for k in dcr_2d if not k.startswith("__")][0]]
                break
if dcr_2d is None: raise FileNotFoundError("No matching DCR file found.")

# === Load LCR ===
lcr_2d = None
for fname in os.listdir(folder):
    if fname.startswith("LCR") and fname.endswith(".mat"):
        m = re.search(r"LCR_\d+_(\d{2,3}(?:\.\d+)?)_(\d+?)_(\d+)\.mat", fname)
        if m:
            v, wl, t = float(m.group(1)), int(m.group(2)), int(m.group(3))
            if v == target_voltage and wl == target_wavelength and t == target_exposure:
                lcr_2d = loadmat(os.path.join(folder, fname))
                lcr_2d = lcr_2d[[k for k in lcr_2d if not k.startswith("__")][0]]
                break
if lcr_2d is None: raise FileNotFoundError("No matching LCR file found.")

shape = dcr_2d.shape

# === Load photon flux ===
wl_list, photonflux_list = get_incident_photons(mat_file, calib_file)
photonflux_dict = dict(zip(wl_list, photonflux_list))
photon_in = photonflux_dict.get(target_wavelength, None)
if photon_in is None: raise ValueError("Photon flux not found for selected wavelength.")

# === PDP calculation ===
net_2d = np.clip(lcr_2d - dcr_2d, 0, None)
pdp_2d = (net_2d / photon_in) * 100

# === ROTATE 2D for intuitive viewing ===
pdp_2d = np.rot90(pdp_2d)

# === Interactive ROI selection and live plot ===
fig, (ax_img, ax_cdf) = plt.subplots(1, 2, figsize=(16, 8))

# Plot full CDF initially
flat_pdp = pdp_2d.flatten()
flat_pdp = flat_pdp[~np.isnan(flat_pdp)]
sorted_full = np.sort(flat_pdp)
x_full = np.linspace(0, 100, len(sorted_full), endpoint=False)
cdf_line, = ax_cdf.plot(x_full, sorted_full, label="Full PDP CDF")
ax_cdf.set_title("PDP CDF", fontsize=18)
ax_cdf.set_xlabel("Pixel Percentile (%)", fontsize=16)
ax_cdf.set_ylabel("PDP (%)", fontsize=16)
ax_cdf.grid(True)
ax_cdf.legend(fontsize=12)

# Show PDP map
img = ax_img.imshow(pdp_2d, cmap='hot')
rect_patch = plt.Rectangle((0, 0), 1, 1, edgecolor='cyan', facecolor='none', lw=2)
ax_img.add_patch(rect_patch)
ax_img.set_title("PDP Heat Map", fontsize=16)
plt.colorbar(img, ax=ax_img, fraction=0.025, pad=0.04)

# === Callback for ROI update ===
def onselect(eclick, erelease):
    x0, y0 = int(eclick.xdata), int(eclick.ydata)
    x1, y1 = int(erelease.xdata), int(erelease.ydata)
    xmin, xmax = sorted([x0, x1])
    ymin, ymax = sorted([y0, y1])

    # Draw rectangle on the map
    rect_patch.set_bounds(xmin, ymin, xmax - xmin, ymax - ymin)

    # Extract PDP values from ROI
    roi = pdp_2d[ymin:ymax, xmin:xmax]
    roi = roi[~np.isnan(roi)]
    if len(roi) == 0:
        return

    roi_sorted = np.sort(roi)
    cdf_x = np.linspace(0, 100, len(roi_sorted), endpoint=False)
    cdf_line.set_data(cdf_x, roi_sorted)

    # Update CDF title with count and percentage
    total_pixels = pdp_2d.size - np.isnan(pdp_2d).sum()
    selected_pixels = len(roi)
    percent_selected = (selected_pixels / total_pixels) * 100
    ax_cdf.set_title(f"PDP CDF — ROI: {selected_pixels}/{total_pixels} pixels "
                     f"({percent_selected:.2f}%)", fontsize=16)

    ax_cdf.relim()
    ax_cdf.autoscale_view()
    fig.canvas.draw_idle()


# === Enable ROI selection ===
roi_selector = RectangleSelector(ax_img, onselect,
                                 useblit=True,
                                 button=[1], minspanx=5, minspany=5,
                                 spancoords='pixels')

# === Add TextBox widgets for PDP min/max ===
axbox_min = plt.axes([0.25, 0.02, 0.1, 0.04])
axbox_max = plt.axes([0.40, 0.02, 0.1, 0.04])
text_box_min = TextBox(axbox_min, 'PDP Min', initial='0')
text_box_max = TextBox(axbox_max, 'PDP Max', initial='100')

def update_clim(_):
    try:
        vmin = float(text_box_min.text)
        vmax = float(text_box_max.text)

        # Update color scale of the heatmap
        img.set_clim(vmin=vmin, vmax=vmax)

        # Update CDF y-axis
        ax_cdf.set_ylim(vmin, vmax)

        fig.canvas.draw_idle()
    except ValueError:
        print("Invalid input: please enter valid numbers.")


text_box_min.on_submit(update_clim)
text_box_max.on_submit(update_clim)


plt.tight_layout()
plt.show()
