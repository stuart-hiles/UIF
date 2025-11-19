#!/usr/bin/env python
"""
uif_quasar_variability_operators.py

Compute linear “operator” fits for the quasar DRW variability sample:

  - log10(tau_days) vs log10(M_BH)
  - log10(tau_days) vs M_i_abs
  - log10(sigma_mag_per_sqrt_yr) vs M_i_abs

for three redshift bins (low-z, mid-z, high-z).

Output:
  output/quasar_variability_experiment/quasar_variability_operators.csv
"""

import os
import numpy as np
import pandas as pd

# ---------------------------------------------------------------------
# 1. Paths (relative to where this script lives)
# ---------------------------------------------------------------------
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# We now read from the *output* catalogue you already generated:
DATA_CSV = os.path.join(
    BASE_DIR,
    "output",
    "quasar_variability_experiment",
    "quasar_variability_i.csv",
)

OUT_DIR = os.path.join(BASE_DIR, "output", "quasar_variability_experiment")
os.makedirs(OUT_DIR, exist_ok=True)

OUT_PATH = os.path.join(OUT_DIR, "quasar_variability_operators.csv")

print(f"Base dir : {BASE_DIR}")
print(f"Input    : {DATA_CSV}")
print(f"Output   : {OUT_PATH}")

# ---------------------------------------------------------------------
# 2. Load catalogue
# ---------------------------------------------------------------------
df = pd.read_csv(DATA_CSV)

# Expected columns (from quasar_variability_i.csv)
z        = df["z"].values
logMBH   = df["log10_M_BH"].values
Mi_abs   = df["M_i_abs"].values
tau      = df["log10_tau_days"].values
sigma    = df["log10_sigma_mag_per_sqrtyr"].values

# Simple quality cuts
mask = (
    np.isfinite(z) &
    np.isfinite(logMBH) &
    np.isfinite(Mi_abs) &
    np.isfinite(tau) &
    np.isfinite(sigma) &
    (tau > -5) &
    (sigma > -5)
)
df = df.loc[mask].copy()
print(f"After basic cuts: {len(df)} objects")

# ---------------------------------------------------------------------
# 3. Define redshift bins
# ---------------------------------------------------------------------
z_edges  = [0.0, 1.0, 1.5, 4.0]
z_labels = ["low-z", "mid-z", "high-z"]
df["z_bin"] = pd.cut(df["z"], bins=z_edges, labels=z_labels, include_lowest=True)

# ---------------------------------------------------------------------
# 4. Utility for linear fits
# ---------------------------------------------------------------------
def linear_fit(x, y):
    m = np.isfinite(x) & np.isfinite(y)
    x = np.asarray(x[m])
    y = np.asarray(y[m])
    n = x.size
    if n < 10:
        return np.nan, np.nan, n
    slope, intercept = np.polyfit(x, y, 1)
    return float(slope), float(intercept), int(n)

rows = []

# ---------------------------------------------------------------------
# 5. Loop over z-bins and compute relations
# ---------------------------------------------------------------------
for zbin in z_labels:
    sub = df[df["z_bin"] == zbin]
    if sub.empty:
        continue
    print(f"\n=== {zbin} ===  (n={len(sub)})")

    # tau vs log10(M_BH)
    s, a, n = linear_fit(sub["log10_M_BH"].values, sub["log10_tau_days"].values)
    print(f"tau~MBH {zbin}: slope={s:.5f}, intercept={a:.5f}, n={n}")
    rows.append({"relation": "tau~MBH", "zbin": zbin, "slope": s, "intercept": a, "n": n})

    # tau vs Mi_abs
    s, a, n = linear_fit(sub["M_i_abs"].values, sub["log10_tau_days"].values)
    print(f"tau~iMag {zbin}: slope={s:.5f}, intercept={a:.5f}, n={n}")
    rows.append({"relation": "tau~iMag", "zbin": zbin, "slope": s, "intercept": a, "n": n})

    # sigma vs Mi_abs
    s, a, n = linear_fit(sub["M_i_abs"].values, sub["log10_sigma_mag_per_sqrtyr"].values)
    print(f"sigma~iMag {zbin}: slope={s:.5f}, intercept={a:.5f}, n={n}")
    rows.append({"relation": "sigma~iMag", "zbin": zbin, "slope": s, "intercept": a, "n": n})

# ---------------------------------------------------------------------
# 6. Write operator table
# ---------------------------------------------------------------------
op = pd.DataFrame(rows, columns=["relation", "zbin", "slope", "intercept", "n"])
op.to_csv(OUT_PATH, index=False)
print(f"\nSaved operator table with {len(op)} rows to:\n  {OUT_PATH}")
print(op)