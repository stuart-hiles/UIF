#!/usr/bin/env python
"""
uif_quasar_variability_operators.py

Extract UIF-style operator *proxies* from the DRW-based quasar variability
catalog:

    output/quasar_variability_experiment/quasar_variability_i.csv

For each redshift bin (low-z, mid-z, high-z) we compute:

    DeltaI_sigma_std        ~ std(log10_sigma_mag_per_sqrtyr)
    Gamma_tau_MB_slope      ~ slope of log10_tau_days vs log10_M_BH
    lambdaR_highR_fraction  ~ fraction of objects with R_proxy > 1
    Rinf_log10sigma_p95     ~ 95th percentile of log10_sigma_mag_per_sqrtyr
    k_tau_spread            ~ (p95 - p05) of log10_tau_days

These follow the UIF intuition:

    DeltaI   → spread of amplitudes (informational difference)
    Gamma    → strength of scaling of tau with mass (recursion / integration)
    lambdaR  → how many objects are in the "high-coherence" regime
    Rinf     → effective coherence ceiling
    k        → spread of timescales (relaxation / recharge proxy)

Usage:
    cd <...>/Unified Theory/Python/Variability
    python uif_quasar_variability_operators.py
"""

from pathlib import Path
import numpy as np
import pandas as pd


# ----------------------------------------------------------------------
# Paths
# ----------------------------------------------------------------------

BASE = Path(__file__).resolve().parent
CAT_PATH = BASE / "output" / "quasar_variability_experiment" / "quasar_variability_i.csv"
OUT_DIR  = BASE / "output" / "quasar_variability_experiment"
OUT_FILE = OUT_DIR / "quasar_variability_operators.csv"

print(f"Base dir : {BASE}")
print(f"Input    : {CAT_PATH}")
print(f"Output   : {OUT_FILE}")

if not CAT_PATH.exists():
    raise FileNotFoundError(f"Cannot find catalog CSV:\n  {CAT_PATH}")

OUT_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(CAT_PATH)

# Required columns from the DRW catalog
required = [
    "z",
    "log10_tau_days",
    "log10_sigma_mag_per_sqrtyr",
    "log10_M_BH",
]
missing = [c for c in required if c not in df.columns]
if missing:
    raise ValueError(f"Missing required columns in CSV: {missing}")

# Clean NaNs for the fields we’ll actually use
mask = (
    df["z"].notna()
    & df["log10_tau_days"].notna()
    & df["log10_sigma_mag_per_sqrtyr"].notna()
)
df = df.loc[mask].copy()
print(f"Usable rows after basic cleaning: {len(df)}")

# ----------------------------------------------------------------------
# Redshift binning (rebuild to be consistent with other scripts)
# ----------------------------------------------------------------------

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

# ----------------------------------------------------------------------
# Recompute R_proxy (normalised coherence amplitude)
# ----------------------------------------------------------------------

sigma_log = df["log10_sigma_mag_per_sqrtyr"].astype(float).values
sigma_lin = 10.0 ** sigma_log  # σ in linear space (mag / sqrt(yr))
sigma_med = np.nanmedian(sigma_lin)
R_proxy = sigma_lin / sigma_med
df["R_proxy"] = R_proxy

# ----------------------------------------------------------------------
# Helper: robust quantiles
# ----------------------------------------------------------------------

def pquantile(x: np.ndarray, q: float) -> float:
    x = np.asarray(x, float)
    x = x[np.isfinite(x)]
    if x.size == 0:
        return np.nan
    return float(np.quantile(x, q))


# ----------------------------------------------------------------------
# Operator proxies per redshift bin
# ----------------------------------------------------------------------

rows = []
bins = ["low-z", "mid-z", "high-z"]

for zbin in bins:
    sub = df[df["zbin"] == zbin].copy()
    n_total = len(sub)
    if n_total == 0:
        print(f"[{zbin}] empty bin, skipping.")
        continue

    print(f"\n=== {zbin} ===")
    print(f"Rows in bin: {n_total}")

    # --- ΔI: spread of coherence amplitudes (sigma log-space) --------------
    sigma_log_sub = sub["log10_sigma_mag_per_sqrtyr"].astype(float).values
    DeltaI_sigma_std = float(np.nanstd(sigma_log_sub))

    # --- Γ: slope of log10_tau_days vs log10_M_BH ---------------------------
    # Use only rows with finite BH mass
    m_mass = sub["log10_M_BH"].notna() & np.isfinite(sub["log10_M_BH"])
    n_mass = int(m_mass.sum())
    if n_mass >= 30:  # need some minimum
        x_mass = sub.loc[m_mass, "log10_M_BH"].astype(float).values
        y_tau  = sub.loc[m_mass, "log10_tau_days"].astype(float).values
        slope, intercept = np.polyfit(x_mass, y_tau, 1)
        Gamma_tau_MB_slope = float(slope)
    else:
        Gamma_tau_MB_slope = np.nan
        print(f"  Not enough BH masses in {zbin} (n={n_mass}) for Γ; set to NaN.")

    # --- λ_R: fraction of sources with R_proxy > 1 -------------------------
    R_sub = sub["R_proxy"].astype(float).values
    n_valid_R = np.isfinite(R_sub).sum()
    if n_valid_R > 0:
        frac_highR = float((R_sub > 1.0).sum() / n_valid_R)
    else:
        frac_highR = np.nan
    lambdaR_highR_fraction = frac_highR

    # --- R∞: 95th percentile of log10_sigma (coherence ceiling) ------------
    Rinf_log10sigma_p95 = pquantile(sigma_log_sub, 0.95)

    # --- k: DRW timescale spread (p95 - p05 of log10_tau_days) -------------
    tau_log_sub = sub["log10_tau_days"].astype(float).values
    tau_p05 = pquantile(tau_log_sub, 0.05)
    tau_p95 = pquantile(tau_log_sub, 0.95)
    k_tau_spread = float(tau_p95 - tau_p05)

    rows.append(
        {
            "zbin": zbin,
            "N": n_total,
            "DeltaI_sigma_std": DeltaI_sigma_std,
            "Gamma_tau_MB_slope": Gamma_tau_MB_slope,
            "lambdaR_highR_fraction": lambdaR_highR_fraction,
            "Rinf_log10sigma_p95": Rinf_log10sigma_p95,
            "k_tau_spread": k_tau_spread,
        }
    )

# ----------------------------------------------------------------------
# Save table
# ----------------------------------------------------------------------

if rows:
    out = pd.DataFrame(rows)
    out.to_csv(OUT_FILE, index=False)
    print("\n=== Operator proxies written to ===")
    print(f"   {OUT_FILE}\n")
    print("Final table:")
    print(out)
else:
    print("No operator rows were generated (something went wrong).")