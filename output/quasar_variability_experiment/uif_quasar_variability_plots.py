#!/usr/bin/env python3
"""
uif_quasar_variability_plots.py

Plots for the UIF quasar variability experiment, consistent with the
quasar scaling / cosmology-lite figures:

1) log10(tau) vs log10(M_BH) in three redshift bins.
2) log10(tau) vs absolute i-band magnitude M_i_abs.
3) log10(sigma) vs M_i_abs.

Input:
    ../output/quasar_variability_experiment/quasar_variability_i.csv

Output (in the same output folder):
    Fig_quasar_tau_vs_MBH.png
    Fig_quasar_tau_vs_Mi.png
    Fig_quasar_sigma_vs_Mi.png
"""

import os
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# ---------------------------------------------------------------------
# 1. Paths
# ---------------------------------------------------------------------
HERE = Path(__file__).resolve().parent
BASE = HERE.parents[1]          # .../UIF
OUT_DIR = BASE / "output" / "quasar_variability_experiment"
CSV_PATH = OUT_DIR / "quasar_variability_i.csv"

print(f"Base dir : {BASE}")
print(f"CSV path : {CSV_PATH}")
print(f"Output   : {OUT_DIR}")

if not CSV_PATH.exists():
    raise FileNotFoundError(f"Cannot find input CSV:\n  {CSV_PATH}")

OUT_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------
# 2. Load data and clean columns
# ---------------------------------------------------------------------
df = pd.read_csv(CSV_PATH)

# Handle duplicated 'z' columns (from master + DRW)
z_cols = [c for c in df.columns if c.strip() == "z"]
if not z_cols:
    raise KeyError("No 'z' column found in quasar_variability_i.csv")
if len(z_cols) > 1:
    print(f"Warning: multiple 'z' columns found {z_cols}; using the first one.")
z = df[z_cols[0]]
df["z_use"] = pd.to_numeric(z, errors="coerce")

# Core columns
# These should exist as per the build script:
#   log10_M_BH (log10 of M_BH/Msun, may be 0.0 if unknown)
#   log10_tau_days
#   log10_sigma_mag_per_sqrtyr
#   M_i_abs (absolute i-band magnitude)
for col in ["log10_M_BH", "log10_tau_days",
            "log10_sigma_mag_per_sqrtyr", "M_i_abs"]:
    if col not in df.columns:
        raise KeyError(f"Expected column '{col}' not found in CSV.")
    df[col] = pd.to_numeric(df[col], errors="coerce")

# ---------------------------------------------------------------------
# 3. Define redshift bins (approximate, can be tuned)
# ---------------------------------------------------------------------
def assign_zbin(zval):
    """
    Basic redshift binning, chosen to roughly match the
    low / mid / high splits used in the slope fits.
    Adjust edges if you want exact counts.
    """
    if zval < 0.8:
        return "low-z"
    elif zval < 1.5:
        return "mid-z"
    else:
        return "high-z"

df["z_bin"] = df["z_use"].apply(assign_zbin)

print("\nRow counts by z_bin:")
print(df["z_bin"].value_counts())

# ---------------------------------------------------------------------
# 4. Helpers for plotting
# ---------------------------------------------------------------------
COLORS = {
    "low-z": "tab:blue",
    "mid-z": "tab:orange",
    "high-z": "tab:green",
}

def scatter_with_fit(ax, x, y, label, color, alpha=0.4):
    """Scatter + simple linear fit line."""
    # Drop NaNs
    mask = np.isfinite(x) & np.isfinite(y)
    if mask.sum() < 5:
        ax.scatter(x, y, s=10, alpha=alpha, color=color, label=f"{label} (n={mask.sum()})")
        return None, None
    xx = x[mask]
    yy = y[mask]
    ax.scatter(xx, yy, s=8, alpha=alpha, color=color, label=f"{label} (n={mask.sum()})")

    # Fit y = m x + c
    m, c = np.polyfit(xx, yy, 1)
    xs = np.linspace(xx.min(), xx.max(), 100)
    ax.plot(xs, m * xs + c, color=color, lw=2)
    return m, c

# ---------------------------------------------------------------------
# 5. Plot log10(tau) vs log10(M_BH)
# ---------------------------------------------------------------------
fig1, ax1 = plt.subplots(figsize=(7, 5))

for zbin in ["low-z", "mid-z", "high-z"]:
    sub = df[(df["z_bin"] == zbin) & (df["log10_M_BH"] > 0)]
    if sub.empty:
        continue
    x = sub["log10_M_BH"].values
    y = sub["log10_tau_days"].values
    m, c = scatter_with_fit(ax1, x, y, zbin, COLORS[zbin])
    if m is not None:
        print(f"tau~MBH fit [{zbin}]: slope={m:.3f}, intercept={c:.3f}, n={len(sub)}")

ax1.set_xlabel(r"$\log_{10}(M_{\mathrm{BH}}/M_{\odot})$")
ax1.set_ylabel(r"$\log_{10}(\tau_{\mathrm{DRW}} / \mathrm{days})$")
ax1.set_title("Quasar DRW Timescale vs Black-Hole Mass (UIF variability sample)")
ax1.grid(alpha=0.3)
ax1.legend(frameon=False)

fig1.tight_layout()
out_fig1 = OUT_DIR / "Fig_quasar_tau_vs_MBH.png"
fig1.savefig(out_fig1, dpi=300)
plt.close(fig1)
print(f"Saved: {out_fig1}")

# ---------------------------------------------------------------------
# 6. Plot log10(tau) vs M_i_abs
# ---------------------------------------------------------------------
fig2, ax2 = plt.subplots(figsize=(7, 5))

for zbin in ["low-z", "mid-z", "high-z"]:
    sub = df[(df["z_bin"] == zbin)]
    if sub.empty:
        continue
    x = sub["M_i_abs"].values
    y = sub["log10_tau_days"].values
    m, c = scatter_with_fit(ax2, x, y, zbin, COLORS[zbin])
    if m is not None:
        print(f"tau~M_i fit [{zbin}]: slope={m:.3f}, intercept={c:.3f}, n={len(sub)}")

# Convention: more negative M_i → brighter, so x-axis reversed
ax2.set_xlabel(r"$M_i$ (absolute i-band magnitude)")
ax2.set_ylabel(r"$\log_{10}(\tau_{\mathrm{DRW}} / \mathrm{days})$")
ax2.set_title("Quasar DRW Timescale vs Luminosity")
ax2.grid(alpha=0.3)
ax2.legend(frameon=False)
ax2.invert_xaxis()

fig2.tight_layout()
out_fig2 = OUT_DIR / "Fig_quasar_tau_vs_Mi.png"
fig2.savefig(out_fig2, dpi=300)
plt.close(fig2)
print(f"Saved: {out_fig2}")

# ---------------------------------------------------------------------
# 7. Plot log10(sigma) vs M_i_abs
# ---------------------------------------------------------------------
fig3, ax3 = plt.subplots(figsize=(7, 5))

for zbin in ["low-z", "mid-z", "high-z"]:
    sub = df[(df["z_bin"] == zbin)]
    if sub.empty:
        continue
    x = sub["M_i_abs"].values
    y = sub["log10_sigma_mag_per_sqrtyr"].values
    m, c = scatter_with_fit(ax3, x, y, zbin, COLORS[zbin])
    if m is not None:
        print(f"sigma~M_i fit [{zbin}]: slope={m:.3f}, intercept={c:.3f}, n={len(sub)}")

ax3.set_xlabel(r"$M_i$ (absolute i-band magnitude)")
ax3.set_ylabel(r"$\log_{10}(\sigma_{\mathrm{DRW}} / \mathrm{mag}\,\mathrm{yr}^{-1/2})$")
ax3.set_title("Quasar DRW Amplitude vs Luminosity")
ax3.grid(alpha=0.3)
ax3.legend(frameon=False)
ax3.invert_xaxis()

fig3.tight_layout()
out_fig3 = OUT_DIR / "Fig_quasar_sigma_vs_Mi.png"
fig3.savefig(out_fig3, dpi=300)
plt.close(fig3)
print(f"Saved: {out_fig3}")

print("\nDone.")