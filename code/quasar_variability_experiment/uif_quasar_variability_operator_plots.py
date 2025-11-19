#!/usr/bin/env python
"""
uif_quasar_variability_operator_plots.py

Make bar plots of UIF-style operators vs redshift bin for the
quasar DRW variability experiment.

Input:
    output/quasar_variability_experiment/quasar_variability_operators.csv

Output (all under the same folder):
    quasar_variability_op_DeltaI.png
    quasar_variability_op_Gamma.png
    quasar_variability_op_lambdaR.png
    quasar_variability_op_Rinf.png
    quasar_variability_op_k.png
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# -------------------------- Paths --------------------------

BASE_DIR = Path(__file__).resolve().parent
IN_PATH = BASE_DIR / "output" / "quasar_variability_experiment" / "quasar_variability_operators.csv"
OUT_DIR = BASE_DIR / "output" / "quasar_variability_experiment"

print(f"Base dir : {BASE_DIR}")
print(f"Input    : {IN_PATH}")
print(f"Output   : {OUT_DIR}")

if not IN_PATH.exists():
    raise FileNotFoundError(f"Cannot find operator CSV at:\n  {IN_PATH}")

OUT_DIR.mkdir(parents=True, exist_ok=True)


# -------------------------- Load data --------------------------

df = pd.read_csv(IN_PATH)

# Ensure the z-bins are in a consistent order
order = ["low-z", "mid-z", "high-z"]
df["zbin"] = pd.Categorical(df["zbin"], categories=order, ordered=True)
df = df.sort_values("zbin")

print("Loaded operator table:")
print(df)


# -------------------------- Helper: bar plot --------------------------

def simple_bar_plot(x_labels, values, ylabel, title, out_path, ylim=None, fmt="{:.3f}"):
    """
    Make a simple 3-bar plot with numeric labels on top.
    """
    x = np.arange(len(x_labels))

    plt.figure(figsize=(5.0, 4.0))
    bars = plt.bar(x, values, color=["tab:blue", "tab:orange", "tab:green"], alpha=0.85)

    # put values on top of bars
    for bar, val in zip(bars, values):
        height = bar.get_height()
        ha = "center"
        va = "bottom" if height >= 0 else "top"
        offset = 0.02 * (max(values) - min(values) if max(values) != min(values) else 1.0)
        plt.text(
            bar.get_x() + bar.get_width() / 2.0,
            height + (offset if height >= 0 else -offset),
            fmt.format(val),
            ha=ha,
            va=va,
            fontsize=9,
        )

    plt.xticks(x, x_labels)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(axis="y", alpha=0.25, linestyle="--", linewidth=0.6)

    if ylim is not None:
        plt.ylim(ylim)

    plt.tight_layout()
    plt.savefig(out_path, dpi=200)
    plt.close()
    print(f"Saved plot: {out_path}")


# -------------------------- Extract columns --------------------------

zlabels = df["zbin"].tolist()

DeltaI_vals = df["DeltaI_sigma_std"].to_numpy()
Gamma_vals  = df["Gamma_tau_MB_slope"].to_numpy()
lambdaR_vals = df["lambdaR_highR_fraction"].to_numpy()
Rinf_vals   = df["Rinf_log10sigma_p95"].to_numpy()
k_vals      = df["k_tau_spread"].to_numpy()


# -------------------------- Make plots --------------------------

# 1. ΔI (sigma std)
simple_bar_plot(
    zlabels,
    DeltaI_vals,
    ylabel=r"$\Delta I$ (σ spread in $\log_{10}\sigma$)",
    title="UIF ΔI vs redshift bin (quasar variability)",
    out_path=OUT_DIR / "quasar_variability_op_DeltaI.png",
    fmt="{:.3f}",
)

# 2. Γ (tau–MBH slope)
simple_bar_plot(
    zlabels,
    Gamma_vals,
    ylabel=r"$\Gamma$ (slope of $\tau$ vs $M_{\mathrm{BH}}$)",
    title="UIF Γ vs redshift bin (quasar variability)",
    out_path=OUT_DIR / "quasar_variability_op_Gamma.png",
    fmt="{:.4f}",
)

# 3. λ_R (fraction of high-R objects)
simple_bar_plot(
    zlabels,
    lambdaR_vals,
    ylabel=r"$\lambda_R$ (fraction of high-coherence quasars)",
    title=r"UIF $\lambda_R$ vs redshift bin (quasar variability)",
    out_path=OUT_DIR / "quasar_variability_op_lambdaR.png",
    ylim=(0.0, 1.0),
    fmt="{:.3f}",
)

# 4. R_inf (95th percentile of log10 σ)
simple_bar_plot(
    zlabels,
    Rinf_vals,
    ylabel=r"$R_\infty$ (95th percentile of $\log_{10}\sigma$)",
    title=r"UIF $R_\infty$ vs redshift bin (quasar variability)",
    out_path=OUT_DIR / "quasar_variability_op_Rinf.png",
    fmt="{:.3f}",
)

# 5. k (τ spread – “memory width”)
simple_bar_plot(
    zlabels,
    k_vals,
    ylabel=r"$k$ (spread in $\log_{10}\tau$)",
    title="UIF k vs redshift bin (quasar variability)",
    out_path=OUT_DIR / "quasar_variability_op_k.png",
    fmt="{:.3f}",
)

print("All operator plots generated.")