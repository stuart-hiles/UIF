# plot_gamma_2x2.py
import os, numpy as np, matplotlib.pyplot as plt

IN  = "ut26_cosmo3d_outputs/gamma_sweep.csv"
OUT = "ut26_cosmo3d_outputs/Fig_gamma_sweep_2x2.png"

if not os.path.exists(IN):
    raise FileNotFoundError(f"Missing sweep file: {IN} (run run_gamma_sweep.py first)")

data = np.genfromtxt(IN, delimiter=",", names=True)
A  = data['A']                      # drive amplitude
W  = data['W']                      # angular frequency (rad/step)
MS = data['final_mean_s']           # final mean coherence
PR = data['total_prunes']           # total prunes (activity)

f = W/(2*np.pi)  # frequency in cycles/step

A_vals = np.unique(A)
f_vals = np.unique(np.round(f, 6))

Prunes   = np.full((len(A_vals), len(f_vals)), np.nan)
MeanS    = np.full((len(A_vals), len(f_vals)), np.nan)
PrunesLn = np.full((len(A_vals), len(f_vals)), np.nan)

for i,a in enumerate(A_vals):
    mA = (A==a)
    fA, msA, prA = np.round(f[mA],6), MS[mA], PR[mA]
    for j,fv in enumerate(f_vals):
        m = (fA==fv)
        if np.any(m):
            Prunes[i,j]   = float(np.mean(prA[m]))
            MeanS [i,j]   = float(np.mean(msA[m]))
            PrunesLn[i,j] = float(np.mean(np.log10(np.maximum(prA[m],1.0))))

# refined collapse criterion (sensitive):
median_prunes = np.nanmedian(Prunes)
Collapse = (np.abs(MeanS - 0.5) > 0.001) | (Prunes < 0.9*median_prunes)
Collapse = Collapse.astype(float)

fig, ax = plt.subplots(2,2, figsize=(10,8))
(ax11, ax12), (ax21, ax22) = ax

extent=[f_vals.min(), f_vals.max(), A_vals.min(), A_vals.max()]

# 1) Total prunes
im1 = ax11.imshow(Prunes, origin='lower', aspect='auto', extent=extent, cmap='magma')
ax11.set_title("(A) Total prunes (activity)")
ax11.set_xlabel("frequency f (cycles/step)")
ax11.set_ylabel("drive amplitude A")
c1 = fig.colorbar(im1, ax=ax11, fraction=0.046, pad=0.04)
c1.set_label("total_prunes")

# 2) Final mean s (tight range)
vmin, vmax = np.nanmin(MeanS), np.nanmax(MeanS)
pad = max(1e-4, 0.05*(vmax - vmin))
im2 = ax12.imshow(MeanS, origin='lower', aspect='auto', extent=extent,
                  cmap='viridis', vmin=vmin-pad, vmax=vmax+pad)
ax12.set_title("(B) Final mean coherence ⟨s⟩")
ax12.set_xlabel("frequency f (cycles/step)")
ax12.set_ylabel("drive amplitude A")
c2 = fig.colorbar(im2, ax=ax12, fraction=0.046, pad=0.04)
c2.set_label("⟨s⟩")

# 3) Refined collapse
im3 = ax21.imshow(Collapse, origin='lower', aspect='auto', extent=extent,
                  cmap='Greens', vmin=0, vmax=1)
ax21.set_title("(C) Refined collapse (1=yes, 0=no)")
ax21.set_xlabel("frequency f (cycles/step)")
ax21.set_ylabel("drive amplitude A")
c3 = fig.colorbar(im3, ax=ax21, fraction=0.046, pad=0.04)
c3.set_label("collapse")

# 4) log10 prunes (for dynamic range)
im4 = ax22.imshow(PrunesLn, origin='lower', aspect='auto', extent=extent,
                  cmap='plasma')
ax22.set_title("(D) log10(total prunes)")
ax22.set_xlabel("frequency f (cycles/step)")
ax22.set_ylabel("drive amplitude A")
c4 = fig.colorbar(im4, ax=ax22, fraction=0.046, pad=0.04)
c4.set_label("log10(prunes)")

plt.suptitle("γ-sweep heatmaps across drive amplitude (A) and frequency (f)", y=0.98, fontsize=12)
plt.tight_layout(rect=[0,0,1,0.97])
plt.savefig(OUT, dpi=200)
plt.close()
print("wrote:", OUT)