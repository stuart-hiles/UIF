# =============================================================
# UIF Paper V — Figure 5.1
# Quasars in the Complexity–Entropy (C–H) Plane
# Generates both a colour-by-redshift and a monochrome version
# =============================================================
import os
import pandas as pd
import matplotlib.pyplot as plt

# ---------- Input / output ----------
infile = "quasar_raw_HC_all.csv"
outdir = "figures"
os.makedirs(outdir, exist_ok=True)

# ---------- Load data ----------
df = pd.read_csv(infile)
print(f"Loaded {len(df)} quasars from {infile}")

# ---------- Extract columns ----------
H = df["H"].astype(float)
C = df["C"].astype(float)
z = df["z"].astype(float)

# Normalise complexity for visual consistency
C_norm = (C - C.min()) / (C.max() - C.min())

# ---------- Figure 5.1a — Colour by redshift ----------
plt.figure(figsize=(7, 6))
sc = plt.scatter(H, C_norm, c=z, cmap="plasma", s=12, alpha=0.7, edgecolor="none")

cb = plt.colorbar(sc)
cb.set_label("Redshift  $z$", fontsize=11)
cb.ax.tick_params(labelsize=9)

plt.xlabel("Spectral Entropy  $H$", fontsize=12)
plt.ylabel("Normalised Lempel–Ziv Complexity  $C_{norm}$", fontsize=12)
plt.title("Quasars in the Complexity–Entropy ($C$–$H$) Plane", fontsize=13)
plt.grid(alpha=0.25)
plt.tight_layout()

outpath_color = os.path.join(outdir, "Fig_5-1a_quasar_CH_plane_color.png")
plt.savefig(outpath_color, dpi=300)
plt.close()
print(f"Saved: {outpath_color}")

# ---------- Figure 5.1b — Monochrome version ----------
plt.figure(figsize=(7, 6))
plt.scatter(H, C_norm, s=10, color="royalblue", alpha=0.65, edgecolor="none")

plt.xlabel("Spectral Entropy  $H$", fontsize=12)
plt.ylabel("Normalised Lempel–Ziv Complexity  $C_{norm}$", fontsize=12)
plt.title("Quasars in the Complexity–Entropy ($C$–$H$) Plane", fontsize=13)
plt.grid(alpha=0.25)
plt.tight_layout()

outpath_mono = os.path.join(outdir, "Fig_5-1b_quasar_CH_plane_mono.png")
plt.savefig(outpath_mono, dpi=300)
plt.close()
print(f"Saved: {outpath_mono}")