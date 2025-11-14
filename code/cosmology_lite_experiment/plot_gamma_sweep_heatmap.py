# plot_gamma_sweep_heatmap.py
import os, numpy as np, matplotlib.pyplot as plt

IN  = "ut26_cosmo3d_outputs/gamma_sweep.csv"
OUT = "ut26_cosmo3d_outputs/Fig_gamma_sweep_heatmap.png"

if not os.path.exists(IN):
    raise FileNotFoundError(f"Missing sweep file: {IN} (run run_gamma_sweep.py first)")

# load sweep
data = np.genfromtxt(IN, delimiter=",", names=True)
A  = data['A']                      # drive amplitude
W  = data['W']                      # angular frequency (rad/step)
MS = data['final_mean_s']           # final mean coherence
PR = data['total_prunes']           # total prunes (activity)

# frequency in cycles/step
f = W / (2*np.pi)

# grids
A_vals = np.unique(A)
f_vals = np.unique(np.round(f, 6))

Prunes = np.full((len(A_vals), len(f_vals)), np.nan)
MeanS  = np.full((len(A_vals), len(f_vals)), np.nan)

for i, a in enumerate(A_vals):
    mA  = (A == a)
    fA  = np.round(f[mA], 6)
    msA = MS[mA]
    prA = PR[mA]
    for j, fv in enumerate(f_vals):
        m = (fA == fv)
        if np.any(m):
            Prunes[i, j] = float(np.mean(prA[m]))
            MeanS [i, j] = float(np.mean(msA[m]))

# refined collapse criterion:
# (i) small but meaningful mean-s drift from 0.5 OR
# (ii) prune suppression relative to the overall median
median_prunes = np.nanmedian(Prunes)
Collapse = (np.abs(MeanS - 0.5) > 0.001) | (Prunes < 0.9 * median_prunes)
Collapse = Collapse.astype(float)  # 1/0 map

# ---- plotting ----
fig, ax = plt.subplots(1, 3, figsize=(14, 4.6))

# Panel 1: Total prunes (activity map)
im0 = ax[0].imshow(Prunes, origin='lower', aspect='auto',
                   extent=[f_vals.min(), f_vals.max(), A_vals.min(), A_vals.max()],
                   cmap='magma')
ax[0].set_xlabel("frequency f (cycles/step)")
ax[0].set_ylabel("drive amplitude A")
ax[0].set_title("Total prunes (activity)")
c0 = fig.colorbar(im0, ax=ax[0], fraction=0.046, pad=0.04)
c0.set_label("total_prunes")

# Panel 2: final mean s (tight range)
vmin = np.nanmin(MeanS); vmax = np.nanmax(MeanS)
# widen a tiny bit to avoid banding
pad = max(1e-4, 0.05*(vmax - vmin))
im1 = ax[1].imshow(MeanS, origin='lower', aspect='auto',
                   extent=[f_vals.min(), f_vals.max(), A_vals.min(), A_vals.max()],
                   cmap='viridis', vmin=vmin - pad, vmax=vmax + pad)
ax[1].set_xlabel("frequency f (cycles/step)")
ax[1].set_ylabel("drive amplitude A")
ax[1].set_title("Final mean coherence <s>")
c1 = fig.colorbar(im1, ax=ax[1], fraction=0.046, pad=0.04)
c1.set_label("<s>")

# Panel 3: refined collapse flag
im2 = ax[2].imshow(Collapse, origin='lower', aspect='auto',
                   extent=[f_vals.min(), f_vals.max(), A_vals.min(), A_vals.max()],
                   cmap='Greens', vmin=0, vmax=1)
ax[2].set_xlabel("frequency f (cycles/step)")
ax[2].set_ylabel("drive amplitude A")
ax[2].set_title("Refined collapse (1=yes, 0=no)")
c2 = fig.colorbar(im2, ax=ax[2], fraction=0.046, pad=0.04)
c2.set_label("collapse")

plt.tight_layout()
plt.savefig(OUT, dpi=160)
plt.close()
print("wrote:", OUT)