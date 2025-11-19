#!/usr/bin/env python3
"""
uif_quasar_variability_scaling.py
---------------------------------
UIF quasar variability — DRW scaling relations (Option 1).

This script reads the merged DRW + master catalog:
    ./output/quasar_variability_experiment/quasar_variability_i.csv

and fits simple linear relations in log–log / linear form:

    log10_tau_days            ~ log10_M_BH
    log10_tau_days            ~ M_i_abs
    log10_sigma_mag_per_sqrtyr ~ M_i_abs

for three redshift bins:
    low-z  : z < 1
    mid-z  : 1 ≤ z < 2
    high-z : z ≥ 2

Outputs:
    ./output/quasar_variability_experiment/UT26_quasar_scaling_slopes.csv

Columns:
    relation,zbin,slope,intercept,n

This is the UIF “quasar scaling” part of the variability experiment.
"""

import os
import numpy as np
import pandas as pd

# ---------------------------------------------------------------------
# 1. Paths (relative to this script)
# ---------------------------------------------------------------------
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
IN_PATH = os.path.join(
    BASE_DIR,
    "output",
    "quasar_variability_experiment",
    "quasar_variability_i.csv",
)
OUT_PATH = os.path.join(
    BASE_DIR,
    "output",
    "quasar_variability_experiment",
    "UT26_quasar_scaling_slopes.csv",
)

print("Base directory:", BASE_DIR)
print("Input file    :", IN_PATH)
print("Output file   :", OUT_PATH)

# ---------------------------------------------------------------------
# 2. Load data
# ---------------------------------------------------------------------
if not os.path.exists(IN_PATH):
    raise FileNotFoundError(f"Could not find input file:\n  {IN_PATH}")

df = pd.read_csv(IN_PATH)
print("Loaded rows:", len(df))

# ---------------------------------------------------------------------
# 3. Column resolution helpers
# ---------------------------------------------------------------------

def resolve_z_column(df: pd.DataFrame) -> str:
    """
    Try to pick the 'best' redshift column.
    We expect either:
      - 'z'
      - or 'redshift'
      - or a duplicated 'z.1' from the merge.
    """
    candidates = ["z", "redshift", "z_drw", "z_master"]
    # Also include any z.* columns
    candidates.extend([c for c in df.columns if c.startswith("z.")])
    for c in candidates:
        if c in df.columns:
            print(f"Using redshift column: {c}")
            return c
    raise KeyError("No suitable redshift column found in variability CSV.")

def resolve_column(df: pd.DataFrame, names, label):
    """
    Generic resolver: given a list of possible column names, pick the first
    that exists. Raise if none found.
    """
    for c in names:
        if c in df.columns:
            print(f"Using {label} column: {c}")
            return c
    raise KeyError(f"No suitable column found for {label}. Tried: {names}")

# Resolve key columns
z_col = resolve_z_column(df)
tau_col = resolve_column(
    df,
    ["log10_tau_days", "log10_tau", "log10_tau_d"],
    "log10_tau_days",
)
sigma_col = resolve_column(
    df,
    ["log10_sigma_mag_per_sqrtyr", "log10_sigma", "log10_sigma_mag_sqrtyr"],
    "log10_sigma_mag_per_sqrtyr",
)
mass_col = resolve_column(
    df,
    ["log10_M_BH", "mass_BH"],
    "log10_M_BH",
)
Mi_col = resolve_column(
    df,
    ["M_i_abs", "M_i"],
    "M_i_abs",
)

# ---------------------------------------------------------------------
# 4. Basic cleaning
# ---------------------------------------------------------------------

# We’ll require finite values for each regression we perform
df_clean = df.copy()

# Coerce to numeric explicitly (in case CSV carried odd types)
for col in [z_col, tau_col, sigma_col, mass_col, Mi_col]:
    df_clean[col] = pd.to_numeric(df_clean[col], errors="coerce")

# Optional: we can also filter to “good” DRW fits if desired, e.g.
# edge_flag == 0 and Plike > Pnoise, etc., but for now we just drop NaNs.
print("Non-NaN counts:")
print(df_clean[[z_col, tau_col, sigma_col, mass_col, Mi_col]].notna().sum())

# ---------------------------------------------------------------------
# 5. Utility: linear fit and logging
# ---------------------------------------------------------------------

def fit_relation(x, y):
    """
    Fit y = a * x + b via least squares using numpy.polyfit.
    Returns (slope, intercept, n).
    """
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    mask = np.isfinite(x) & np.isfinite(y)
    x = x[mask]
    y = y[mask]
    n = x.size
    if n < 10:
        # too few points to trust a slope
        return np.nan, np.nan, n
    slope, intercept = np.polyfit(x, y, 1)
    return float(slope), float(intercept), int(n)

# Redshift binning
def z_bin_label(z):
    if z < 1.0:
        return "low-z"
    elif z < 2.0:
        return "mid-z"
    else:
        return "high-z"

df_clean["zbin"] = df_clean[z_col].apply(z_bin_label)

# ---------------------------------------------------------------------
# 6. Perform fits for each relation & z-bin
# ---------------------------------------------------------------------

results = []

def add_fit(relation_name, x_col, y_col):
    """
    For a given relation y_col ~ x_col, fit separate lines in each z-bin.
    Append results to the global 'results' list.
    """
    for zbin in ["low-z", "mid-z", "high-z"]:
        sub = df_clean[df_clean["zbin"] == zbin]
        x = sub[x_col]
        y = sub[y_col]
        slope, intercept, n = fit_relation(x, y)
        print(f"[{relation_name}, {zbin}] slope={slope:.4f} (n={n})")
        results.append(
            {
                "relation": relation_name,
                "zbin": zbin,
                "slope": slope,
                "intercept": intercept,
                "n": n,
            }
        )

# 6.1 τ ~ M_BH
add_fit("tau~MBH", mass_col, tau_col)

# 6.2 τ ~ M_i_abs
add_fit("tau~iMag", Mi_col, tau_col)

# 6.3 σ ~ M_i_abs
add_fit("sigma~iMag", Mi_col, sigma_col)

# ---------------------------------------------------------------------
# 7. Write scaling summary to CSV
# ---------------------------------------------------------------------
res_df = pd.DataFrame(results)
res_df.to_csv(OUT_PATH, index=False)

print("\n=== Scaling results written to ===")
print("  ", OUT_PATH)
print("\nResult preview:")
print(res_df)