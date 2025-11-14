# =============================================================
# UIF Paper V — Figure 5.1
# Quasars in the Complexity–Entropy (C–H) Plane
# =============================================================
import os
import pandas as pd
import matplotlib.pyplot as plt

# ---------- Load the CSV ----------
infile = "quasar_raw_HC_all.csv"
outpng = os.path.join("figures", "Fig_5-1_quasar_CH_plane.png")
os.makedirs("figures", exist_ok=True)

df = pd.read_csv(infile)
print(f"Loaded {len(df)} quasars")

# ---------- Extract columns ----------
H = df["H"].astype(float)
C = df["C"].astype(float)

# Normalise C for plotting consistency
C_norm = (C - C.min()) / (C.max() - C.min())

# ---------- Optional colour by redshift ----------
z = df["z"].astype(float)

# ---------- Plot ----------
plt.figure(figsize=(7,6))
sc = plt.scatter(H, C_norm, c=z, cmap="plasma", s=10, alpha=0.7, edgecolor="none")

cb = plt.colorbar(sc)
cb.set_label("Redshift $z$")

plt.xlabel("Spectral Entropy  $H$")
plt.ylabel("Normalised Lempel–Ziv Complexity  $C_{norm}$")
plt.title("Quasars in the Complexity–Entropy ($C$–$H$) Plane")

plt.grid(alpha=0.25)
plt.tight_layout()
plt.savefig(outpng, dpi=300)
plt.show()

print(f"Saved: {outpng}")
