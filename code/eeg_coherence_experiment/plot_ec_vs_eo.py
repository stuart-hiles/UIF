# Plot EC vs EO scatter and EC-EO histogram (robust to string cols)
import os, json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

SUB_FILE = "outputs/EEG_subject_summary_R.csv"
RES_FILE = "outputs/EEG_effects_EC_vs_EO.json"
OUT_SCAT = "outputs/Fig_EC_vs_EO.png"
OUT_HIST = "outputs/Fig_EC_minus_EO_hist.png"

def main():
    if not (os.path.exists(SUB_FILE) and os.path.exists(RES_FILE)):
        print("Missing inputs:", SUB_FILE, RES_FILE); return

    sub = pd.read_csv(SUB_FILE)
    with open(RES_FILE) as f:
        res = json.load(f)

    xo = pd.to_numeric(sub.get("eyes_open"), errors="coerce")
    xc = pd.to_numeric(sub.get("eyes_closed"), errors="coerce")
    valid = (~xo.isna()) & (~xc.isna())
    xo = xo[valid].values
    xc = xc[valid].values

    # Scatter: EC vs EO
    plt.figure(figsize=(6,6))
    plt.scatter(xo, xc, c="tab:blue", s=40, alpha=0.7, edgecolor="none")
    vmin = float(min(xo.min(), xc.min())); vmax = float(max(xo.max(), xc.max()))
    pad  = 0.02*(vmax - vmin) if vmax > vmin else 0.05
    lims = [vmin - pad, vmax + pad]
    plt.plot(lims, lims, "k--", lw=1)
    plt.xlim(lims); plt.ylim(lims)
    plt.xlabel("R (Eyes Open)"); plt.ylabel("R (Eyes Closed)")
    plt.title(f"Subject-level EC vs EO (n={res.get('n_subjects','?')})")
    plt.grid(alpha=0.3); plt.tight_layout()
    plt.savefig(OUT_SCAT, dpi=150); plt.close(); print("wrote:", OUT_SCAT)

    # Histogram: EC - EO
    diffs = (xc - xo)  # EC - EO
    ci = res.get("CI95_bootstrap", [np.nan, np.nan, np.nan])
    mean_diff = float(np.mean(diffs))
    pval = res.get("p_perm_two_sided", None)

    plt.figure(figsize=(6,4))
    plt.hist(diffs, bins=14, color="tab:green", alpha=0.75)
    for x in [ci[0], ci[2]]:
        if np.isfinite(x): plt.axvline(x, color="k", linestyle="--", lw=1)
    plt.axvline(mean_diff, color="r", lw=2, label=f"mean={mean_diff:.3f}")
    if pval is not None:
        plt.title(f"EC − EO: mean={mean_diff:.3f}, d={res.get('cohen_d_paired',np.nan):.2f}, p={pval:.3f}")
    else:
        plt.title(f"EC − EO: mean={mean_diff:.3f}, d={res.get('cohen_d_paired',np.nan):.2f}")

    plt.xlabel("R (EC − EO)"); plt.ylabel("Subjects")
    plt.legend(); plt.grid(alpha=0.3); plt.tight_layout()
    plt.savefig(OUT_HIST, dpi=150); plt.close(); print("wrote:", OUT_HIST)

if __name__ == "__main__":
    main()