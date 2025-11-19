#!/usr/bin/env python
"""
uif_quasar_variability_hc.py

Builds HC-like (H–C) planes and “coherence” histograms for the
UIF quasar DRW-based variability catalog:

    output/quasar_variability_experiment/quasar_variability_i.csv

This is a *diagnostic* HC-plane for the DRW-compressed dataset.
We approximate per-object “H” and “C” from the joint distribution
of log10_tau_days and log10_sigma_* (the DRW sigma-amplitude column),
rather than using true time-series H and C as in the original Stripe-82
HC experiment.

Outputs (all under output/quasar_variability_experiment/):

    quasar_variability_HC_all.png
    quasar_variability_HC_lowz.png
    quasar_variability_HC_midz.png
    quasar_variability_HC_highz.png

    quasar_variability_R_hist_zbins.png

    quasar_variability_hc_summary.csv  # per-z bin mean/std of H,C,R proxies

Usage:
    Run from the Variability project folder:

        cd path/to/…/Python/Variability
        python uif_quasar_variability_hc.py
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


# -------------------------- Paths & config --------------------------

BASE = Path(__file__).resolve().parent
DATA_PATH = BASE / "output" / "quasar_variability_experiment" / "quasar_variability_i.csv"
OUT_DIR   = BASE / "output" / "quasar_variability_experiment"

NBINS_HC = 40          # 2D histogram bins for H/C
MIN_POINTS_PER_BIN = 200  # minimum N per z-bin for plotting


# -------------------------- Load data --------------------------

print(f"Base dir : {BASE}")
print(f"CSV path : {DATA_PATH}")
print(f"Output   : {OUT_DIR}")

if not DATA_PATH.exists():
    raise FileNotFoundError(f"Cannot find input CSV:\n  {DATA_PATH}")

OUT_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(DATA_PATH)

# We require at least z and log10_tau_days; the sigma column name we will detect.
required_cols = [
    "z",
    "log10_tau_days",
]
missing = [c for c in required_cols]  # will refine below

for c in required_cols:
    if c not in df.columns:
        raise ValueError(f"Missing required column in CSV: {c}")

# Detect the DRW sigma-amplitude column automatically.
# We expect something like 'log10_sigma_mag_sqrtyr' or 'log10_sigma_mag_per_sqrtyr'.
sigma_candidates = [c for c in df.columns if "log10_sigma_mag" in c]
if len(sigma_candidates) == 0:
    raise ValueError(
        "Could not find a sigma-amplitude column. "
        "Expected a column containing 'log10_sigma_mag', e.g. 'log10_sigma_mag_sqrtyr' or 'log10_sigma_mag_per_sqrtyr'."
    )
elif len(sigma_candidates) > 1:
    # If there are multiple matches, you can refine this logic if needed.
    raise ValueError(
        f"Multiple possible sigma columns found: {sigma_candidates}. "
        "Please keep only one amplitude column or adjust the detection logic."
    )

SIGMA_COL = sigma_candidates[0]
print(f"Using sigma-amplitude column: {SIGMA_COL}")

# Drop rows with NaNs in the core DRW parameters
mask = ~df["z"].isna() & ~df["log10_tau_days"].isna() & ~df[SIGMA_COL].isna()
df = df.loc[mask].copy()
print(
    f"Using {len(df)} rows after dropping NaNs in "
    f"[z, log10_tau_days, {SIGMA_COL}]."
)

# -------------------------- Redshift binning --------------------------

z = df["z"].values
z1, z2 = np.quantile(z, [1/3, 2/3])
print(f"Redshift quantiles: z1={z1:.3f}, z2={z2:.3f}")

def assign_zbin(zval: float) -> str:
    if zval < z1:
        return "low-z"
    elif zval < z2:
        return "mid-z"
    else:
        return "high-z"

df["zbin"] = df["z"].apply(assign_zbin)

# -------------------------- Proxy H, C, R definitions --------------------------

# DRW parameters
tau = df["log10_tau_days"].values       # log10 τ (days)
sig = df[SIGMA_COL].values             # log10 σ (mag / sqrt(yr))

# "Coherence" proxy R: linearised sigma, normalised by its median.
sigma_lin = 10.0 ** sig
R = sigma_lin / np.nanmedian(sigma_lin)
df["R_proxy"] = R

# Build a 2D histogram over (tau, sig) to define a density-based H proxy
print("Building 2D histogram for H/C proxy...")
valid = ~np.isnan(tau) & ~np.isnan(sig)
x = tau[valid]
y = sig[valid]

H2d, xedges, yedges = np.histogram2d(x, y, bins=NBINS_HC)
P = H2d.astype(float)
P_sum = P.sum()
if P_sum <= 0:
    raise RuntimeError("2D histogram is empty; check data / filters.")
P /= P_sum

# Avoid log(0) by masking empty bins
with np.errstate(divide="ignore", invalid="ignore"):
    surprisal = -np.log2(P)  # bits
surprisal[P <= 0] = np.nan

Smax = np.nanmax(surprisal)
print(f"Max surprisal (H_max) in 2D grid: {Smax:.3f} bits")

# Map each data point to its bin, then to H_proxy and C_proxy
ix = np.searchsorted(xedges, df["log10_tau_days"].values, side="right") - 1
iy = np.searchsorted(yedges, df[SIGMA_COL].values,       side="right") - 1

in_bounds = (ix >= 0) & (ix < NBINS_HC) & (iy >= 0) & (iy < NBINS_HC)

H_proxy = np.full(len(df), np.nan, dtype=float)
C_proxy = np.full(len(df), np.nan, dtype=float)

H_proxy[in_bounds] = surprisal[ix[in_bounds], iy[in_bounds]]

# Normalise H into [0,1], then define a simple LMC-style complexity proxy:
#   C = 4 * H_norm * (1 - H_norm)
H_norm = H_proxy / Smax
H_norm = np.clip(H_norm, 0.0, 1.0)
C_proxy[in_bounds] = 4.0 * H_norm[in_bounds] * (1.0 - H_norm[in_bounds])

df["H_proxy"] = H_norm
df["C_proxy"] = C_proxy

print("Proxy H/C/R columns added: [H_proxy, C_proxy, R_proxy]")


# -------------------------- HC plane plots --------------------------

def plot_hc_all(df: pd.DataFrame, out_path: Path):
    """Plot H vs C for all objects, colored by redshift."""
    plt.figure(figsize=(6.5, 5.5))
    m = ~df["H_key"].isna() if "H_key" in df.columns else ~df["H_proxy"].isna()
    m = ~df["H_proxy"].isna() & ~df["C_proxy"].isna() & ~df["z"].isna()
    sub = df.loc[m]

    sc = plt.scatter(
        sub["H_proxy"].values,
        sub["C_proxy"].values,
        c=sub["z"].values,
        s=5,
        cmap="viridis",
        alpha=0.7,
        edgecolors="none",
    )
    cbar = plt.gca().figure.colorbar(sc)
    cbar.set_label("redshift z", fontsize=10)

    plt.xlabel("H_proxy (normalised surprisal)")
    plt.ylabel("C_proxy (LMC-like complexity)")
    plt.title("Quasar DRW HC-like plane — all redshifts")
    plt.grid(alpha=0.2, linestyle="--", linewidth=0.5)
    plt.tight_layout()
    plt.savefig(out_path, dpi=200)
    plt.close()
    print(f"Saved: {out_path}")


def plot_hc_by_zbin(df: pd.DataFrame, out_prefix: Path):
    """Plot H–C scatter per redshift bin, colored by log10 sigma (amplitude)."""
    for zbin in ["low-z", "mid-z", "high-z"]:
        sub = df[(df["zbin"] == zbin) & (~df["H_proxy"].isna()) & (~df["C_proxy"].isna())]
        n = len(sub)
        if n < MIN_POINTS_PER_BIN:
            print(f"[{zbin}] only {n} points; skipping HC plot.")
            continue

        plt.figure(figsize=(6.0, 5.5))
        sc = plt.scatter(
            sub["H_proxy"].values,
            sub["C_proxy"].values,
            c=sub[SIGMA_COL].values,
            s=6,
            cmap="plasma",
            alpha=0.7,
            edgecolors="none",
        )
        cbar = plt.colorbar(sc)
        cbar.set_label(r"$\log_{10}\,\sigma_{\mathrm{mag}/\sqrt{\mathrm{yr}}}$", fontsize=10)
        plt.xlabel("H_proxy (normalised surprisal)")
        plt.ylabel("C_proxy (LMC-like complexity)")
        plt.title(f"HC-like plane — {zbin} (N={n})")
        plt.grid(alpha=0.2, linestyle="--", linewidth=0.5)
        plt.tight_layout()

        out_path = out_prefix.parent / f"{out_prefix.stem}_{zbin}.png"
        plt.savefig(out_path, dpi=200)
        plt.close()
        print(f"[{zbin}] saved HC-like plane: {out_path}")


# -------------------------- “Coherence” histograms --------------------------

def plot_coherence_histograms(df: pd.DataFrame, out_path: Path):
    """
    Plot histograms of the DRW log10 sigma-amplitude column (coherence proxy)
    in three redshift bins: low / mid / high.
    """
    plt.figure(figsize=(7.5, 4.5))

    bins = 40
    colors = {"low-z": "tab:blue", "mid-z": "tab:orange", "high-z": "tab:green"}

    for zbin in ["low-z", "mid-z", "high-z"]:
        sub = df[df["zbin"] == zbin]
        vals = sub[SIGMA_COL].dropna().values
        n = len(vals)
        plt.hist(
            vals,
            bins=bins,
            alpha=0.6,
            label=f"{zbin} (N={n})",
            density=True,
            color=colors.get(zbin, None),
            histtype="discrete" if n < 50 else "stepfilled",
        )

    plt.xlabel(r"$\log_{10}\,\sigma_{\mathrm{mag}/\sqrt{\mathrm{yr}}}$")
    plt.ylabel("Density")
    plt.title("Quasar DRW amplitude (sigma) distribution by redshift bin")
    plt.legend()
    plt.grid(alpha=0.2, linestyle="--", linewidth=0.5)
    plt.tight_layout()
    plt.savefig(out_path, dpi=200)
    plt.close()
    print(f"Saved coherence histograms: {out_path}")


# -------------------------- Summary stats per z-bin --------------------------

def compute_hc_summary(df: pd.DataFrame, out_path: Path):
    rows = []
    for zbin in ["low-z", "mid-z", "high-z"]:
        sub = df[df["zbin"] == zbin]
        m = ~sub["H_proxy"].isna()
        if m.sum() == 0:
            continue
        s = sub.loc[m]
        rows.append(
            {
                "zbin": zbin,
                "N": len(s),
                "H_mean": float(s["H_proxy"].mean()),
                "H_std": float(s["H_proxy"].std()),
                "C_mean": float(s["C_proxy"].mean()),
                "C_std": float(s["C_proxy"].std()),
                "R_mean": float(s["R_proxy"].mean()),
                "R_std": float(s["R_proxy"].std()),
            }
        )
    if not rows:
        print("No valid rows for HC summary; skipping.")
        return
    out = pd.DataFrame(rows)
    out.to_csv(out_path, index=False)
    print(f"Saved HC summary stats: {out_path}")


# -------------------------- Run all steps --------------------------

if __name__ == "__main__":
    print("Generating HC-like planes and coherence diagnostics for DRW-based quasar variability...")

    # Global HC plane (all z, colored by z)
    plot_hc_all(df, OUT_DIR / "quasar_variability_HC_all.png")

    # HC per redshift bin (colored by sigma amplitude)
    plot_hc_by_zbin(df, OUT_DIR / "quasar_variability_HC")

    # “Coherence” histograms (sigma-amplitude per z-bin)
    plot_coherence_histograms(df, OUT_DIR / "quasar_variability_R_hist_zbins.png")

    # Summary CSV for later operator-level use
    compute_hc_summary(df, OUT_DIR / "quasar_variability_hc_summary.csv")

    print("Done.")