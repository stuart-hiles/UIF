#!/usr/bin/env python
"""
uif_quasar_variability_operators_plots.py

Reads UIF operator estimates for the quasar variability experiment and
produces:

  1) A radar "fingerprint" plot showing the relative shape of the
     operator vector (ΔI, Γ, λ_R, R_∞, k) for each redshift bin.

  2) A 5-panel bar grid showing each operator vs redshift bin with
     numeric annotations.

Input (relative to this script):
    output/quasar_variability_experiment/quasar_variability_operators.csv

Output:
    output/quasar_variability_experiment/quasar_variability_operators_radar.png
    output/quasar_variability_experiment/quasar_variability_operators_bars.png
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# ----------------------- Paths -----------------------

BASE = Path(__file__).resolve().parent
CAT_PATH = BASE / "output" / "quasar_variability_experiment" / "quasar_variability_operators.csv"
OUT_DIR  = BASE / "output" / "quasar_variability_experiment"

print(f"Base dir : {BASE}")
print(f"Input    : {CAT_PATH}")
print(f"Output   : {OUT_DIR}")

if not CAT_PATH.exists():
    raise FileNotFoundError(f"Cannot find operator CSV:\n  {CAT_PATH}")

OUT_DIR.mkdir(parents=True, exist_ok=True)

# ------------------- Load operators -------------------

df = pd.read_csv(CAT_PATH)

required_cols = [
    "zbin",
    "DeltaI_sigma_std",
    "Gamma_tau_MB_slope",
    "lambdaR_highR_fraction",
    "Rinf_log10sigma_p95",
    "k_tau_spread",
]
missing = [c for c in required_cols if c not in df.columns]
if missing:
    raise ValueError(f"Missing columns in operator CSV: {missing}")

# we expect exactly three bins: low-z, mid-z, high-z
zbins_order = ["low-z", "mid-z", "high-z"]
df = df.set_index("zbin").loc[zbins_order].reset_index()

# For convenience, rename into shorter operator symbols
df_ops = df.rename(
    columns={
        "DeltaI_sigma_std": "DeltaI",
        "Gamma_tau_MB_slope": "Gamma",
        "lambdaR_highR_fraction": "lambdaR",
        "Rinf_log10sigma_p95": "Rinf",
        "k_tau_spread": "k",
    }
)

print("Loaded operator table:")
print(df_ops)

# operator columns and pretty labels
op_cols = ["DeltaI", "Gamma", "lambdaR", "Rinf", "k"]
op_labels = [r"$\Delta I$", r"$\Gamma$", r"$\lambda_R$", r"$R_\infty$", r"$k$"]

# ----------------------- Radar plot -----------------------

def make_radar_plot(df_ops: pd.DataFrame, out_path: Path):
    """
    Make a radar "fingerprint" plot.

    We min-max normalise each operator across z-bins so that the shape
    of each z-bin's operator vector is emphasised.
    """
    # extract raw operator matrix: shape (n_zbins, n_ops)
    values = df_ops[op_cols].values.astype(float)

    # min-max normalise per column
    col_min = values.min(axis=0)
    col_max = values.max(axis=0)
    denom = (col_max - col_min)
    denom[denom == 0.0] = 1.0  # avoid division by zero
    norm_values = (values - col_min) / denom

    n_ops = len(op_cols)
    angles = np.linspace(0, 2 * np.pi, n_ops, endpoint=False)
    # close the loop
    angles = np.concatenate([angles, angles[:1]])

    fig = plt.figure(figsize=(7, 6))
    ax = fig.add_subplot(111, polar=True)

    colors = {
        "low-z": "tab:blue",
        "mid-z": "tab:orange",
        "high-z": "tab:green",
    }

    for i, zbin in enumerate(df_ops["zbin"].values):
        vals = norm_values[i]
        vals_closed = np.concatenate([vals, vals[:1]])
        ax.plot(
            angles,
            vals_closed,
            "-o",
            label=zbin,
            color=colors.get(zbin, None),
            linewidth=2,
            markersize=5,
        )
        ax.fill(angles, vals_closed, alpha=0.15, color=colors.get(zbin, None))

    ax.set_xticks(np.linspace(0, 2 * np.pi, n_ops, endpoint=False))
    ax.set_xticklabels(op_labels, fontsize=12)
    ax.set_ylim(0, 1.0)
    ax.set_yticks([0.25, 0.5, 0.75])
    ax.set_yticklabels(["0.25", "0.5", "0.75"], fontsize=9)
    ax.set_title("UIF operator fingerprint — quasar variability sample", pad=20)

    # small legend showing also the *actual* operator values
    leg_labels = []
    for _, row in df_ops.iterrows():
        z = row["zbin"]
        nums = ", ".join(
            f"{row[c]:.3g}" for c in op_cols
        )
        leg_labels.append(f"{z}: [{nums}]")
    ax.legend(
        leg_labels,
        loc="upper right",
        bbox_to_anchor=(1.35, 1.05),
        fontsize=8,
        frameon=True,
    )

    plt.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Saved radar plot: {out_path}")


# ----------------------- Bar-grid plot -----------------------

def make_bar_grid(df_ops: pd.DataFrame, out_path: Path):
    """
    5-panel bar grid: one panel per operator vs redshift bin.
    """
    fig, axes = plt.subplots(1, 5, figsize=(14, 4), sharey=False)
    colors = ["tab:blue", "tab:orange", "tab:green"]

    z_labels = df_ops["zbin"].values

    for j, (ax, col, label) in enumerate(zip(axes, op_cols, op_labels)):
        vals = df_ops[col].values
        x = np.arange(len(z_labels))

        ax.bar(x, vals, color=colors, alpha=0.8)
        ax.set_xticks(x)
        ax.set_xticklabels(z_labels, rotation=30, ha="right", fontsize=9)
        ax.set_title(label, fontsize=12)

        # y-labels for a couple of panels to avoid clutter
        if j == 0:
            ax.set_ylabel("value")

        # annotate on top of each bar
        for xi, v in zip(x, vals):
            ax.text(
                xi,
                v,
                f"{v:.3g}",
                ha="center",
                va="bottom",
                fontsize=8,
                rotation=0,
            )

        ax.grid(axis="y", alpha=0.2, linestyle="--", linewidth=0.5)

    fig.suptitle("UIF operators vs redshift bin — quasar variability experiment", y=1.02)
    plt.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Saved bar-grid plot: {out_path}")


# ----------------------- Run all -----------------------

if __name__ == "__main__":
    make_radar_plot(df_ops, OUT_DIR / "quasar_variability_operators_radar.png")
    make_bar_grid(df_ops, OUT_DIR / "quasar_variability_operators_bars.png")
    print("Done.")