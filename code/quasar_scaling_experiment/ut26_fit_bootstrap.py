import numpy as np, pandas as pd, matplotlib.pyplot as plt, argparse, json
from math import sqrt
np.set_printoptions(suppress=True)

# ---------- helpers ----------
def lcdm_lookback(z, H0=70.0, Om=0.3, N=1200):
    h = H0/100.0; tH = 9.778/h
    Ol = 1.0 - Om
    def E(zz): return np.sqrt(Om*(1+zz)**3 + Ol)
    if z <= 0: return 0.0
    zz = np.linspace(0, z, N)
    return tH * np.trapz(1/((1+zz)*E(zz)), zz)

def model_A(theta, t): a,b = theta; return a + b*t
def model_B(theta, t): Rinf,k,R0 = theta; return Rinf*(1 - np.exp(-k*t)) + R0
def model_C(theta, t): Rinf,k,t0 = theta; return Rinf/(1 + np.exp(-k*(t - t0)))

def fit_model(fun, theta0, t, y, yerr, max_iter=1500, lr=1e-2):
    w = 1.0/np.maximum(yerr, 1e-6)
    theta = np.array(theta0, dtype=float)
    for _ in range(max_iter):
        yhat = fun(theta, t)
        r = (y - yhat)*w
        # numerical Jacobian
        J = []
        eps = 1e-6
        for i in range(len(theta)):
            d = np.zeros_like(theta); d[i] = eps
            y2 = fun(theta + d, t)
            J.append(((y2 - yhat)/eps)*w)
        J = np.vstack(J).T
        step, *_ = np.linalg.lstsq(J, r, rcond=None)
        theta += lr*step
        if np.linalg.norm(step) < 1e-6: break
    yhat = fun(theta, t)
    resid = (y - yhat)/np.maximum(yerr, 1e-6)
    rss = float(np.sum(resid**2)); n=len(y); p=len(theta)
    aic = n*np.log(rss/n + 1e-12) + 2*p
    bic = n*np.log(rss/n + 1e-12) + p*np.log(max(n,1))
    return theta, rss, aic, bic

def build_R(df):
    H = df["H"].values
    C = df["C"].values
    Cmin, Cmax = np.nanmin(C), np.nanmax(C)
    Cn = (C - Cmin) / (Cmax - Cmin + 1e-12)
    return (1 - H) + Cn

def bin_by_z(df, bins):
    labels = [f"{bins[i]}–{bins[i+1]}" for i in range(len(bins)-1)]
    df = df.copy()
    df["zbin"] = pd.cut(df["z"], bins=bins, labels=labels, include_lowest=True)
    agg = df.groupby("zbin").agg(
        z_mean=("z","mean"),
        R_mean=("R","mean"),
        R_sem=("R", lambda x: np.nanstd(x, ddof=1)/sqrt(max(1, np.sum(~np.isnan(x))))),
        n=("R","count")
    ).dropna()
    agg["t_Gyr"] = agg["z_mean"].apply(lcdm_lookback)
    return df, agg

def bootstrap_bins(df, bins, n_boot=1000, seed=42):
    rng = np.random.default_rng(seed)
    labels = [f"{bins[i]}–{bins[i+1]}" for i in range(len(bins)-1)]
    df = df.copy()
    df["zbin"] = pd.cut(df["z"], bins=bins, labels=labels, include_lowest=True)
    groups = {lab: g for lab,g in df.groupby("zbin")}
    # fixed times per bin (use z_mean from original)
    t_bins = {lab: lcdm_lookback(g["z"].mean()) for lab,g in groups.items()}
    # bootstrap: resample rows within each bin
    out = []
    for b in range(n_boot):
        zs, Rs, ts, ns = [], [], [], []
        for lab, g in groups.items():
            if g.empty: continue
            idx = rng.integers(0, len(g), len(g))
            sample = g.iloc[idx]
            zs.append(sample["z"].mean())
            Rs.append(sample["R"].mean())
            ts.append(t_bins[lab])
            ns.append(len(sample))
        if len(Rs) >= 3:  # need >=3 bins to fit 3-param logistic
            out.append({"t":np.array(ts), "R":np.array(Rs), "n":np.array(ns)})
    return out

# ---------- main ----------
def main():
    ap = argparse.ArgumentParser(description="UT26 bootstrap fits for coherence growth")
    ap.add_argument("--in", type=str, default="ut26_full/quasar_raw_HC_all.csv")
    ap.add_argument("--outdir", type=str, default="ut26_full")
    ap.add_argument("--boots", type=int, default=1000)
    ap.add_argument("--bins", type=str, default="0,0.5,1,1.5,2,3")
    args = ap.parse_args()

    os.makedirs(args.outdir, exist_ok=True)
    df = pd.read_csv(args.__dict__["in"])
    df["R"] = build_R(df)

    bins = list(map(float, args.bins.split(",")))
    dfb, agg = bin_by_z(df, bins)

    # Prepare data vectors
    x = agg["t_Gyr"].values
    y = agg["R_mean"].values
    yerr = np.maximum(agg["R_sem"].values, 1e-6)

    # Fit A/B/C on the binned means
    a0 = y.min(); b0 = (y.max()-y.min())/max(1e-3, x.max()-x.min())
    thetaA, rssA, aicA, bicA = fit_model(model_A, [a0, b0], x, y, yerr)
    thetaB, rssB, aicB, bicB = fit_model(model_B, [y.max(), 0.3, y.min()], x, y, yerr)
    thetaC, rssC, aicC, bicC = fit_model(model_C, [y.max(), 0.3, x.mean()], x, y, yerr)

    summary = pd.DataFrame([
        {"model":"A_linear","params":thetaA.tolist(),"rss":rssA,"AIC":aicA,"BIC":bicA},
        {"model":"B_saturating_exp","params":thetaB.tolist(),"rss":rssB,"AIC":aicB,"BIC":bicB},
        {"model":"C_logistic","params":thetaC.tolist(),"rss":rssC,"AIC":aicC,"BIC":bicC},
    ])
    summary.to_csv(f"{args.outdir}/ut26_model_fits_boot.csv", index=False)

    # Bootstrap logistic C only (the ceiling model)
    boot = bootstrap_bins(dfb, bins, n_boot=args.boots, seed=42)
    thetas = []
    for b in boot:
        tb, Rb = b["t"], b["R"]
        # simple yerr proxy (SEM ~ std/sqrt(n)) from resample; use uniform small err if degenerate
        yerrb = np.full_like(Rb, np.maximum(np.std(Rb)/np.sqrt(len(Rb)), 1e-3))
        try:
            th, *_ = fit_model(model_C, [thetaC[0], thetaC[1], thetaC[2]], tb, Rb, yerrb, max_iter=800, lr=1e-2)
            thetas.append(th)
        except Exception:
            continue

    thetas = np.array(thetas)  # shape (B,3)
    stats = {}
    if thetas.size:
        qs = np.quantile(thetas, [0.025, 0.5, 0.975], axis=0)
        stats = {
            "Rinf_ci": qs[:,0].tolist(),
            "k_ci":    qs[:,1].tolist(),
            "t0_ci":   qs[:,2].tolist(),
            "n_boot_ok": int(len(thetas))
        }
        with open(f"{args.outdir}/ut26_logistic_bootstrap.json","w") as f:
            json.dump(stats, f, indent=2)

        # Plot data + logistic fit + 95% band
        t_fit = np.linspace(0, x.max()*1.05, 400)
        y_med = model_C(qs[1], t_fit)
        y_lo  = model_C(qs[0], t_fit)
        y_hi  = model_C(qs[2], t_fit)

        plt.figure(figsize=(7,5))
        plt.errorbar(x, y, yerr=yerr, fmt='o', capsize=3, label="binned ⟨R⟩")
        plt.plot(t_fit, y_med, label="logistic (median)", color="C2")
        plt.fill_between(t_fit, y_lo, y_hi, color="C2", alpha=0.2, label="95% CI")
        plt.xlabel("Lookback time (Gyr)")
        plt.ylabel("Mean coherence index ⟨R⟩")
        plt.title("UT26 coherence vs cosmic time — logistic fit with 95% CI")
        plt.legend()
        plt.tight_layout()
        plt.savefig(f"{args.outdir}/ut26_coherence_logistic_boot_CI.png", dpi=150)

    # Always write the binned table
    agg.to_csv(f"{args.outdir}/ut26_R_binned_boot.csv", index=False)

    print("[done] wrote:")
    print("  ut26_model_fits_boot.csv")
    print("  ut26_R_binned_boot.csv")
    if stats:
        print("  ut26_logistic_bootstrap.json  (95% CIs)")
        print("  ut26_coherence_logistic_boot_CI.png")
    else:
        print("  (bootstrap had no valid fits; check bins/boots)")

if __name__ == "__main__":
    import os
    main()