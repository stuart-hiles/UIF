# plot_hysteresis.py
import os, numpy as np, matplotlib.pyplot as plt

BASE = "ut26_cosmo3d_outputs"

# auto-detect the latest hysteresis run folder (starts with 'hyst_')
candidates = [d for d in os.listdir(BASE) if os.path.isdir(os.path.join(BASE,d)) and d.startswith("hyst_")]
if not candidates:
    raise FileNotFoundError("No hysteresis run folder found under ut26_cosmo3d_outputs/")
candidates.sort(key=lambda d: os.path.getmtime(os.path.join(BASE,d)))
run_dir = os.path.join(BASE, candidates[-1])

csv_path = os.path.join(run_dir, "hysteresis.csv")
if not os.path.exists(csv_path):
    raise FileNotFoundError(f"Missing {csv_path}")

data = np.genfromtxt(csv_path, delimiter=",", names=True)
t = data["t"]; A = data["A"]; ms = data["mean_s"]; pr = data["prunes"]

# Split phase boundary (assuming uniform logging every SNAP_EVERY)
# Use the largest jump in A as the boundary:
jump_idx = np.argmax(np.abs(np.diff(A)))
cut = jump_idx + 1

fig, ax = plt.subplots(1,3, figsize=(13,4.2))

# Panel 1: A(t)
ax[0].plot(t, A, lw=1.8)
ax[0].set_xlabel("time (steps)")
ax[0].set_ylabel("drive amplitude A")
ax[0].set_title("Drive schedule")

# Panel 2: <s>(t)
ax[1].plot(t, ms, lw=1.8)
ax[1].set_xlabel("time (steps)")
ax[1].set_ylabel("<s>")
ax[1].set_title("Coherence response")

# Panel 3: hysteresis loop <s> vs A
ax[2].plot(A[:cut], ms[:cut], lw=1.8, label="phase 1 (high A)")
ax[2].plot(A[cut:], ms[cut:], lw=1.8, label="phase 2 (low A)")
ax[2].set_xlabel("A")
ax[2].set_ylabel("<s>")
ax[2].set_title("Hysteresis: <s> vs A")
ax[2].legend(frameon=False)

plt.tight_layout()
out_png = os.path.join(run_dir, "Fig_hysteresis.png")
plt.savefig(out_png, dpi=160)
plt.close()
print("wrote:", out_png)
print("from:", run_dir)