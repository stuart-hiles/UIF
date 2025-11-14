# plot_threshold_heatmap.py
import os, numpy as np, matplotlib.pyplot as plt

IN  = "ut26_cosmo3d_outputs/threshold_map.csv"
OUT = "ut26_cosmo3d_outputs/Fig_threshold_map.png"

if not os.path.exists(IN):
    raise FileNotFoundError(f"Missing sweep file: {IN} (run run_threshold_map.py first)")

d = np.genfromtxt(IN, delimiter=",", names=True)
eta, lr, reg = d['eta'], d['lambdaR'], d['regime']

etas, lrs = np.unique(eta), np.unique(lr)
H = np.full((len(etas), len(lrs)), np.nan)
for i,e in enumerate(etas):
    m = (eta==e)
    lr_e, reg_e = lr[m], reg[m]
    for j,L in enumerate(lrs):
        mm = (lr_e==L)
        if np.any(mm):
            H[i,j] = np.mean(reg_e[mm])

plt.figure(figsize=(6,5))
im = plt.imshow(H, origin='lower', aspect='auto',
                extent=[lrs.min(), lrs.max(), etas.min(), etas.max()],
                cmap='viridis', vmin=0, vmax=2)
plt.xlabel("lambda_R (retention)"); plt.ylabel("eta* (collapse threshold)")
plt.title("Goldilocks map: 0=fragile, 1=stable ceiling, 2=runaway")
plt.colorbar(im, fraction=0.046, pad=0.04)
plt.tight_layout()
plt.savefig(OUT, dpi=160); plt.close()
print("wrote:", OUT)