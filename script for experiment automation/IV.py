import time
import pyvisa
import numpy as np
import matplotlib.pyplot as plt
import csv
import os

# ==============================
# User settings
# ==============================
SMU_RESOURCE = "TCPIP0::169.254.5.2::hislip0::INSTR"   # <— update to your SMU VISA address
SAVE_DIR     = r"C:/Users/Admin/OneDrive - epfl.ch/Desktop/py/singleSPAD/108/IV"  # output folder
FILENAME     = "108_-20_L2_iv.txt"

V_START      = 16       # V
V_END        = 22      # V
V_STEP       = 0.025       # V
SETTLING_S   = 0.1       # wait after changing V before measuring
AVG_READS    = 5         # average N readings per bias point
NPLC         = 1.0       # integration time in power-line cycles
I_COMPLIANCE = 5e-3      # A — safety current compliance
USE_4WIRE    = False     # True to enable remote sensing (if wired)

# ==============================
# Build sweep list (one direction only)
# ==============================
voltages = np.arange(V_START, V_END + 1e-12, V_STEP)

# ==============================
# VISA init
# ==============================
rm = pyvisa.ResourceManager()
smu = rm.open_resource(SMU_RESOURCE)
smu.timeout = 15000  # ms
smu.read_termination  = '\n'
smu.write_termination = '\n'
smu.clear()

def smu_write(cmd):
    smu.write(cmd)

def configure_smu():
    smu_write("*RST")
    smu_write("*CLS")
    smu_write("SOUR:FUNC VOLT")
    smu_write("SOUR:VOLT:MODE FIX")
    smu_write("SENS:FUNC 'CURR'")
    smu_write("SENS:CURR:RANG:AUTO ON")
    smu_write(f"SENS:CURR:PROT {I_COMPLIANCE}")
    smu_write(f"SENS:CURR:NPLC {NPLC}")
    smu_write(f"SYST:RSEN {'ON' if USE_4WIRE else 'OFF'}")
    smu_write(f"SOUR:VOLT {V_START}")
    smu_write("OUTP ON")
    time.sleep(0.1)  # short warm-up

def measure_current(v_set):
    smu_write(f"SOUR:VOLT {v_set}")
    time.sleep(SETTLING_S)
    readings = []
    for _ in range(AVG_READS):
        i = float(smu.query("MEAS:CURR?").strip())
        readings.append(i)
        if AVG_READS > 1:
            time.sleep(SETTLING_S / 3)
    arr = np.array(readings, dtype=float)
    return arr.mean(), (arr.std(ddof=1) if len(arr) > 1 else 0.0)

def safe_shutdown():
    try:
        smu_write("SOUR:VOLT 0")
        time.sleep(0.2)
        smu_write("OUTP OFF")
    except Exception:
        pass

def main():
    os.makedirs(SAVE_DIR, exist_ok=True)
    configure_smu()

    v_data = []
    i_data = []
    i_std  = []

    plt.ion()
    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(6, 7))
    ax1.set_ylabel("Current (A)")
    ax1.set_title("SPAD I-V (live)")
    ax2.set_xlabel("Voltage (V)")
    ax2.set_ylabel("|Current| (A)")
    ax2.set_yscale("log")
    line1, = ax1.plot([], [], "o-")
    line2, = ax2.plot([], [], "o-")

    try:
        for v in voltages:
            mean_i, std_i = measure_current(v)
            v_data.append(v)
            i_data.append(mean_i)
            i_std.append(std_i)
            print(f"V = {v:6.3f} V, I = {mean_i: .3e} A  (±{std_i: .1e})")
            line1.set_data(v_data, i_data)
            line2.set_data(v_data, np.abs(i_data))
            ax1.relim(); ax1.autoscale_view()
            ax2.relim(); ax2.autoscale_view()
            plt.pause(0.01)

    except KeyboardInterrupt:
        print("\nInterrupted by user.")
    finally:
        safe_shutdown()
        plt.ioff()
        plt.show()

        save_path = os.path.join(SAVE_DIR, FILENAME)
        with open(save_path, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["Voltage_V", "Current_A", "CurrentStd_A", "NPLC", "I_Comp_A"])
            for v, i, s in zip(v_data, i_data, i_std):
                w.writerow([f"{v:.6f}", f"{i:.12e}", f"{s:.12e}", NPLC, I_COMPLIANCE])
        print(f"\nSaved: {save_path}")

        try:
            smu.close()
            rm.close()
        except Exception:
            pass

if __name__ == "__main__":
    main()
