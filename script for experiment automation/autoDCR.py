import time
import pyvisa
import numpy as np
import matplotlib.pyplot as plt
import os
import sys

# ==============================
# User Settings
# ==============================
V_START = 32.05           # Starting voltage (V)
V_END   = V_START + 2.5     # Ending voltage (V)
V_STEP  = 0.5             # Voltage step (V)
V_BD    = 28.55           # Breakdown voltage (V)
N_READS = 5               # Counter reads per bias point
SAFE_VOLTAGE = 15.0       # Return voltage to this value at the end
SETTLE_PER_VOLTAGE_S = 10 # settle time after setting the voltage

SAVE_DIR = r"C:/Users/Admin/OneDrive - epfl.ch/Desktop/py/singleSPAD/031"

# ---- Gate-time schedule (piecewise). First match wins. ----
# (low_inclusive, high_exclusive, gate_time_seconds)
GATE_SCHEDULE = [
    (32.05, np.inf, 1000.0),
]
DEFAULT_GATE_TIME = 60.0  # fallback

# ----- Overhead model (include all sleeps/latencies) -----
UI_UPDATE_PERIOD_S          = 0.2   # how often to refresh countdown lines
FETCH_MARGIN_S              = 0.10  # small guard before FETCh?
POST_SET_VOLTAGE_OVERHEAD_S = 0.20  # VISA + instrument latency after SOUR:VOLT
PER_FETCH_OVERHEAD_S        = 0.10  # VISA latency per query() round-trip
PER_PLOT_OVERHEAD_S         = 0.15  # time to redraw per voltage (rough average)

def gate_time_for_voltage(v: float) -> float:
    for lo, hi, t in GATE_SCHEDULE:
        if lo <= v < hi:
            return float(t)
    return float(DEFAULT_GATE_TIME)

def format_time(seconds: float) -> str:
    seconds = max(0, int(round(seconds)))
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    return f"{h:02}:{m:02}:{s:02}"

def print_inline(msg: str):
    sys.stdout.write("\r" + msg + " " * 16)
    sys.stdout.flush()

# ----- Compute remaining time from current position -----
def estimate_total_remaining(voltages, v_idx, reads_done, gate_fn, in_gate_remaining_s):
    """
    voltages: list/array of all voltages
    v_idx:    index of current voltage (0-based)
    reads_done: how many reads already completed at this voltage
    in_gate_remaining_s: seconds left to complete the current (active) gate.
                         If idle (between gates), pass 0.
    Returns seconds estimate of all remaining work including overheads.
    """
    rem = 0.0

    # If we are inside a gate at current voltage:
    rem += max(0.0, in_gate_remaining_s) + FETCH_MARGIN_S + PER_FETCH_OVERHEAD_S

    # Remaining reads at current voltage (after the current gate completes)
    if v_idx < len(voltages):
        v = voltages[v_idx]
        gate_t = gate_fn(v)
        reads_left = max(0, N_READS - reads_done - 1)  # exclude the active gate just accounted
        rem += reads_left * (gate_t + FETCH_MARGIN_S + PER_FETCH_OVERHEAD_S)

        # Plot redraw after finishing this voltage (once)
        rem += PER_PLOT_OVERHEAD_S

    # Future voltages
    for v_future in voltages[v_idx+1:]:
        gt = gate_fn(v_future)
        rem += POST_SET_VOLTAGE_OVERHEAD_S
        rem += SETTLE_PER_VOLTAGE_S
        rem += N_READS * (gt + FETCH_MARGIN_S + PER_FETCH_OVERHEAD_S)
        rem += PER_PLOT_OVERHEAD_S

    return rem

# ==============================
# PyVISA setup
# ==============================
rm = pyvisa.ResourceManager()
counter = rm.open_resource("TCPIP0::169.254.2.30::inst0::INSTR")
source  = rm.open_resource("TCPIP0::169.254.5.2::hislip0::INSTR")

# Timeouts (counter timeout updated per-point below)
source.timeout  = 5000  # ms
counter.timeout = 2000  # ms placeholder

# ==============================
# Setup B2910BL as DC voltage source
# ==============================
source.write("*RST")
source.write("SOUR:FUNC VOLT")
source.write("SOUR:VOLT:MODE FIX")
source.write("SOUR:VOLT:RANG 30")
source.write("SOUR:VOLT:ILIM 1e-3")  # Current limit: 1 mA
source.write("OUTP ON")

# ==============================
# Configure Counter (Keysight 53220A)
# ==============================
counter.write("*CLS")
counter.write("ABOR")
counter.write("INP1:COUP AC")
counter.write("INP1:IMP 1E6")
counter.write("INP1:RANG 50")
counter.write("INP1:LEV:AUTO OFF")

# ==============================
# Prepare Plot
# ==============================
plt.ion()
fig, ax = plt.subplots()
ax.set_xlabel("Bias Voltage (V)")
ax.set_ylabel("Average Count Rate (1/s)")
ax.set_title("Live Count vs Bias (mean ± std)")
ax.set_yscale("log")

volt_data, mean_data, std_data, gate_used = [], [], [], []

# ==============================
# Main loop
# ==============================
voltages = np.arange(V_START, V_END + 1e-12, V_STEP)

exp_start = time.perf_counter()

try:
    for v_idx, v in enumerate(voltages):
        print(f"\n--- Bias Voltage: {v:.2f} V ({v_idx+1}/{len(voltages)}) ---")
        source.write(f"SOUR:VOLT {v}")
        # Include VISA/instrument latency overhead explicitly
        time.sleep(POST_SET_VOLTAGE_OVERHEAD_S)

        # Live settle countdown
        settle_end = time.perf_counter() + SETTLE_PER_VOLTAGE_S
        while True:
            now = time.perf_counter()
            if now >= settle_end:
                break
            remaining_settle = settle_end - now
            # Remaining total includes: remaining settle (no gate active) + future work
            total_remaining = remaining_settle + estimate_total_remaining(
                voltages, v_idx, reads_done=0, gate_fn=gate_time_for_voltage, in_gate_remaining_s=0.0
            )
            print_inline(f"Settling {format_time(remaining_settle)} | Total ETA {format_time(total_remaining)}")
            time.sleep(UI_UPDATE_PERIOD_S)
        print_inline("")
        print()

        gate_t = gate_time_for_voltage(v)
        gate_used.append(gate_t)
        counter.write(f"CONF:TOT:TIM {gate_t}")
        counter.timeout = int((gate_t + 5.0) * 1000)  # generous margin

        print(f"Gate Time: {gate_t:.3f} s")

        # Trigger level based on over-bias
        excess_v = v - V_BD
        if excess_v >= 0:
            trig_level = 0.75 * excess_v
            counter.write(f"INP1:LEV {trig_level:.3f}")
            print(f"Trigger level set to {trig_level:.3f} V")
        else:
            print("⚠️  Bias below breakdown — trigger level not set.")

        counts = []
        for i in range(N_READS):
            # Start a timed totalize run
            counter.write("INIT")
            run_start = time.perf_counter()
            run_end   = run_start + gate_t

            # Live per-gate countdown; ETA includes all future work + this gate remainder
            while True:
                now = time.perf_counter()
                if now >= run_end:
                    break
                left_this_gate = run_end - now
                total_remaining = estimate_total_remaining(
                    voltages, v_idx, reads_done=i, gate_fn=gate_time_for_voltage,
                    in_gate_remaining_s=left_this_gate
                )
                print_inline(
                    f"Run {i+1}/{N_READS} | This gate {format_time(left_this_gate)} "
                    f"| Total ETA {format_time(total_remaining)}"
                )
                time.sleep(UI_UPDATE_PERIOD_S)

            # tiny guard + fetch
            print_inline("Fetching result...")
            time.sleep(FETCH_MARGIN_S)
            count_total = float(counter.query("FETCh?").strip())
            counts.append(count_total)
            time.sleep(PER_FETCH_OVERHEAD_S)
            print_inline("")
            print(f"\r  Count {i+1}: {int(count_total)}")

        # Filter obvious outliers
        min_count = min(counts)
        filtered_counts = [c for c in counts if c <= min_count * 10]

        mean_rate = np.mean(filtered_counts) / gate_t
        std_rate  = (np.std(filtered_counts, ddof=1) / gate_t) if len(filtered_counts) > 1 else 0.0

        print(f"→ Mean Count Rate at {v:.2f} V: {mean_rate:.2f} ± {std_rate:.2f}")

        volt_data.append(v)
        mean_data.append(mean_rate)
        std_data.append(std_rate)

        # Update live plot (account for plotting overhead in ETA model via PER_PLOT_OVERHEAD_S)
        ax.clear()
        ax.set_xlabel("Bias Voltage (V)")
        ax.set_ylabel("Average Count Rate (1/s)")
        ax.set_title("Live Count vs Bias (mean ± std)")
        ax.set_yscale("log")
        ax.errorbar(volt_data, mean_data, yerr=std_data, fmt='o-', capsize=3)
        ax.grid(True, which='both', linestyle='--', alpha=0.3)
        fig.tight_layout()
        plt.pause(0.01)

    # After loop, clear final inline line
    print_inline("")
    print()

except KeyboardInterrupt:
    print("\nMeasurement interrupted by user.")

finally:
    print(f"\nResetting bias to {SAFE_VOLTAGE} V for safety...")
    try:
        source.write(f"SOUR:VOLT {SAFE_VOLTAGE}")
        time.sleep(0.5)
        source.write("OUTP OFF")
    except Exception:
        pass

    plt.ioff()
    plt.show()

    if len(volt_data) > 0:
        save_prompt = input("\n💾 Do you want to save the data? (y/n): ").strip().lower()
        if save_prompt == 'y':
            filename = input("Enter filename (no extension): ").strip()
            os.makedirs(SAVE_DIR, exist_ok=True)
            save_path = os.path.join(SAVE_DIR, filename + ".txt")
            with open(save_path, 'w') as f:
                f.write("# Bias Voltage (V)\tGate Time (s)\tMean Count Rate (1/s)\tStd Dev (1/s)\n")
                for v, gt, m, s in zip(volt_data, gate_used, mean_data, std_data):
                    f.write(f"{v:.3f}\t{gt:.6g}\t{m:.6g}\t{s:.6g}\n")
            print(f"\n✅ Data saved to: {save_path}")
        else:
            print("❌ Data not saved.")

    # Cleanly close VISA sessions
    try:
        counter.close()
        source.close()
        rm.close()
    except Exception:
        pass
