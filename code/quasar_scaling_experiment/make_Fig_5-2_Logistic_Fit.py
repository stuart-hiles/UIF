# =============================================================
# UIF Paper V — Figure 5.2
# Logistic fit of quasar coherence vs lookback time (binned)
# Uses ut26_R_binned_boot.csv (t_Gyr, R_mean, R_sem, n)
# Optional: ut26_logistic_bootstrap.json for curve + 95% CI
# =============================================================
import os, json, numpy as np, pandas as pd, matplotlib.pyplot as plt

CSV_IN  = "ut26_R_binned_boot.csv"          # your binned file (screenshot columns)
JSON_IN = "ut26_logistic_bootstrap.json"    # optional; if absent, we plot points+errorbars only
OUTPNG  = os.path.join("figures", "Fig_5-2_quasar_logistic_fit.png")
os.makedirs("figures", exist_ok=True)

# ---------------------------
# Load binned CSV
# ---------------------------
df = pd.read_csv(CSV_IN)
cols = {c.lower(): c for c in df.columns}

# tolerant column resolution
t_col  = cols.get("t_gyr", cols.get("lookback_gyr"))
R_col  = cols.get("r_mean")
SE_col = cols.get("r_sem")   # standard error of mean
n_col  = cols.get("n")       # optional count

if t_col is None or R_col is None:
    raise ValueError(f"Could not find lookback time and/or R columns in {CSV_IN}. "
                     f"Found columns: {list(df.columns)}")

t   = df[t_col].astype(float).values
R   = df[R_col].astype(float).values
Rlo = (R - df[SE_col].astype(float).values) if SE_col else (R - 0.0)
Rhi = (R + df[SE_col].astype(float).values) if SE_col else (R + 0.0)

# ---------------------------
# Try to load bootstrap params (JSON) for logistic curve + CI
# Expected structure:
# {
#   "R_inf":{"median":0.8986,"lo":0.8939,"hi":0.9033},
#   "k":{"median":0.6800,"lo":0.3388,"hi":1.1720},
#   "t0":{"median":0.000,"lo":-5.10,"hi":1.71},
#   "n_boot_ok":1000
# }
# ---------------------------
have_json = os.path.exists(JSON_IN)
if have_json:
    with open(JSON_IN, "r") as f:
        jb = json.load(f)
    R_inf_med = jb["R_inf"]["median"]; R_inf_lo = jb["R_inf"]["lo"]; R_inf_hi = jb["R_inf"]["hi"]
    k_med     = jb["k"]["median"];     k_lo     = jb["k"]["lo"];     k_hi     = jb["k"]["hi"]
    t0_med    = jb["t0"]["median"];    t0_lo    = jb["t0"]["lo"];    t0_hi    = jb["t0"]["hi"]

    # make a smooth time grid spanning your binned points
    tgrid = np.linspace(min(t)-0.3, max(t)+0.3, 300)

    def logistic(tt, Rinf, kk, t0):
        return Rinf / (1.0 + np.exp(-kk*(tt - t0)))

    # median curve
    R_med_curve = logistic(tgrid, R_inf_med, k_med, t0_med)

    # derive 95% CI by sampling params using the JSON lo/hi as ~95% ranges
    # (Gaussian approx: sigma = (hi - lo) / 3.92)
    n_samp = 2000
    def gauss_params(lo, med, hi):
        sigma = (hi - lo) / 3.92 if hi > lo else 0.0
        return np.random.normal(loc=med, scale=max(sigma, 1e-12), size=n_samp)

    Rinf_s = gauss_params(R_inf_lo, R_inf_med, R_inf_hi)
    k_s    = gauss_params(k_lo,     k_med,     k_hi)
    t0_s   = gauss_params(t0_lo,    t0_med,    t0_hi)

    Rsamp = np.empty((n_samp, len(tgrid)))
    for i in range(n_samp):
        Rsamp[i, :] = logistic(tgrid, Rinf_s[i], k_s[i], t0_s[i])
    R_lo_curve = np.percentile(Rsamp, 2.5, axis=0)
    R_hi_curve = np.percentile(Rsamp, 97.5, axis=0)

# ---------------------------
# Plot
# ---------------------------
plt.figure(figsize=(7.0, 5.6))

# 95% CI for the curve (if JSON present)
if have_json:
    plt.fill_between(tgrid, R_lo_curve, R_hi_curve,
                     color="mediumseagreen", alpha=0.25, label="95% CI (curve)")

# median curve
if have_json:
    plt.plot(tgrid, R_med_curve, color="seagreen", lw=2.2, label="logistic (median)")

# binned points with error bars
yerr = None
if SE_col:
    yerr = df[SE_col].values
plt.errorbar(t, R, yerr=yerr, fmt="o", ms=6, color="darkgreen", ecolor="darkseagreen",
             elinewidth=1.2, capsize=3, label="binned ⟨R⟩")

plt.xlabel("Lookback time (Gyr)", fontsize=12)
plt.ylabel("Mean coherence index ⟨R⟩", fontsize=12)
plt.title("Logistic fit to quasar coherence vs cosmic time", fontsize=13)
plt.grid(alpha=0.28)
plt.legend(frameon=False)
plt.tight_layout()
plt.savefig(OUTPNG, dpi=300)
plt.close()
print(f"Saved: {OUTPNG}")