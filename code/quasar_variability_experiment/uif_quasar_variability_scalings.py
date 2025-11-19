#!/usr/bin/env python3
"""
uif_quasar_variability_scalings.py

Compute simple DRW scaling relations from the merged Stripe 82
quasar variability catalog (quasar_variability_i.csv):

  1) log10_tau_days ~ log10_M_BH
  2) log10_tau_days ~ M_i_abs
  3) log10_sigma_mag_per_sqrtyr ~ M_i_abs

for three redshift bins: low-z, mid-z, high-z.

Outputs:
  output/quasar_variability_experiment/quasar_variability_scalings.csv
"""

import os
import numpy as np
import pandas as pd

# --------------------------------------------------------------
# 1. Locate input and output paths
# --------------------------------------------------------------
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Input catalog produced earlier
INPUT_CSV = os.path.join(
    BASE_DIR,
    "output",
    "quasar_variability_experiment",
    "quasar_variability_i.csv"
)

# Output summary CSV
OUT_CSV = os.path.join(
    BASE_DIR,
    "output",
    "quasar_variability_experiment",
    "quasar_variability_scalings.csv"
)

print("Base directory:", BASE_DIR)
print("Input catalog :", INPUT_CSV)
print("Output path   :", OUT_CSV)

# --------------------------------------------------------------
# 2. Load the merged DRW + master catalog
# --------------------------------------------------------------
df = pd.read_csv(INPUT_CSV)

# Sanity: enforce numeric types (in case of stray strings)
numeric_cols = [
    "z",
    "M_i_abs",
    "log10_M_BH",
    "log10_tau_days",
    "log10_sigma_mag_per_sqrtyr",
]
for c in numeric_cols:
    if c in df.columns:
        df[c] = pd.to_numeric(df[c], errors="coerce")

# Drop rows that are totally unusable for all fits
df = df.dropna(subset=["z", "log10_tau_days", "M_i_abs"], how="any")
print(f"Total usable rows after basic cleaning: {len(df)}")

# --------------------------------------------------------------
# 3. Define redshift bins
# --------------------------------------------------------------
# Simple, transparent split:
#   low-z  : z < 1
#   mid-z  : 1 <= z < 2
#   high-z : z >= 2
#
# This is easy to understand and roughly matches standard quasar binning.
def z_bin_label(z):
    if z < 1.0:
        return "low-z"
    elif z < 2.0:
        return "mid-z"
    else:
        return "high-z"

df["zbin"] = df["z"].apply(z_bin_label)

# --------------------------------------------------------------
# 4. Helper: robust linear fit with NaN handling
# --------------------------------------------------------------
def safe_linfit(x, y):
    """
    Fit y = m x + c with NaN filtering.
    Returns (slope, intercept, n_used) or (np.nan, np.nan, 0)
    if too few points.
    """
    x = np.asarray(x)
    y = np.asarray(y)
    mask = np.isfinite(x) & np.isfinite(y)
    x_sel = x[mask]
    y_sel = y[mask]
    n = len(x_sel)
    if n < 10:  # arbitrary: require at least 10 points for a meaningful fit
        return np.nan, np.nan, n
    m, c = np.polyfit(x_sel, y_sel, 1)
    return m, c, n

# --------------------------------------------------------------
# 5. Loop over z bins and fit the three relations
# --------------------------------------------------------------
records = []

for zbin in ["low-z", "mid-z", "high-z"]:
    sub = df[df["zbin"] == zbin]
    if sub.empty:
        print(f"[WARN] No rows in {zbin} bin; skipping.")
        continue

    print(f"\n=== {zbin} ===")
    print(f"Rows in bin: {len(sub)}")

    # 1) log10_tau_days ~ log10_M_BH (where BH mass is available)
    if "log10_M_BH" in sub.columns:
        m1, c1, n1 = safe_linfit(sub["log10_M_BH"], sub["log10_tau_days"])
        print(f"tau~MBH: slope={m1:.6f}, intercept={c1:.6f}, n={n1}")
        records.append({
            "relation": "tau~MBH",
            "zbin": zbin,
            "slope": m1,
            "intercept": c1,
            "n": int(n1),
        })
    else:
        print("tau~MBH: log10_M_BH column not found; skipping.")

    # 2) log10_tau_days ~ M_i_abs
    if "M_i_abs" in sub.columns:
        m2, c2, n2 = safe_linfit(sub["M_i_abs"], sub["log10_tau_days"])
        print(f"tau~iMag: slope={m2:.6f}, intercept={c2:.6f}, n={n2}")
        records.append({
            "relation": "tau~iMag",
            "zbin": zbin,
            "slope": m2,
            "intercept": c2,
            "n": int(n2),
        })
    else:
        print("tau~iMag: M_i_abs column not found; skipping.")

    # 3) log10_sigma_mag_per_sqrtyr ~ M_i_abs
    if "log10_sigma_mag_per_sqrtyr" in sub.columns:
        m3, c3, n3 = safe_linfit(sub["M_i_abs"], sub["log10_sigma_mag_per_sqrtyr"])
        print(f"sigma~iMag: slope={m3:.6f}, intercept={c3:.6f}, n={n3}")
        records.append({
            "relation": "sigma~iMag",
            "zbin": zbin,
            "slope": m3,
            "intercept": c3,
            "n": int(n3),
        })
    else:
        print("sigma~iMag: log10_sigma_mag_per_sqrtyr column not found; skipping.")

# --------------------------------------------------------------
# 6. Write summary CSV
# --------------------------------------------------------------
if records:
    out_df = pd.DataFrame.from_records(records)
    out_df.to_csv(OUT_CSV, index=False)
    print("\nWrote scaling relations to:")
    print("  ", OUT_CSV)
    print("\nFinal table:")
    print(out_df)
else:
    print("\nNo records were generated — check column names and z binning.")