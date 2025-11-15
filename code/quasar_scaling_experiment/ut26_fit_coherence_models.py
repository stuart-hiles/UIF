# ut26_fit_coherence_models.py
import numpy as np, pandas as pd, matplotlib.pyplot as plt

# --- CONFIG ---
IN = "ut26_full/quasar_raw_HC_all.csv"         # <- change if your output dir differs
OUT_BINS = "ut26_full/ut26_R_binned.csv"
OUT_FITS = "ut26_full/ut26_model_fits.csv"
OUT_PNG  = "ut26_full/ut26_coherence_growth_models.png"

# 1) Load H,C,z,iMag
df = pd.read_csv(IN)

# 2) Build coherence index R = (1 - H) + C_norm
H = df["H"].values
C = df["C"].values
C_norm = (C - np.nanmin(C)) / (np.nanmax(C) - np.nanmin(C) + 1e-12)
df["R"] = (1 - H) + C_norm

# 3) Bin by redshift (tweak as desired)
bins = [0.0, 0.5, 1.0, 1.5, 2.0, 3.0]
labels = [f"{bins[i]}–{bins[i+1]}" for i in range(len(bins)-1)]
df["zbin"] = pd.cut(df["z"], bins=bins, labels=labels, include_lowest=True)

from math import sqrt
agg = df.groupby("zbin").agg(
    z_mean=("z","mean"),
    R_mean=("R","mean"),
    R_sem=("R", lambda x: np.nanstd(x, ddof=1) / sqrt(max(1, np.sum(~np.isnan(x)))) ),
    n=("R","count")
).dropna()

# 4) z -> lookback time (Gyr), flat LCDM (H0=70, Om=0.3)
H0 = 70.0; h = H0/100.0; tH = 9.778/h
Om = 0.3; Ol = 1.0 - Om
def E(z): return np.sqrt(Om*(1+z)**3 + Ol)
def lookback_time(z, N=1000):
    if z <= 0: return 0.0
    zz = np.linspace(0, z, N)
    return tH * np.trapz(1/((1+zz)*E(zz)), zz)

agg["t_Gyr"] = agg["z_mean"].apply(lookback_time)

# 5) Fit models vs t
x = agg["t_Gyr"].values
y = agg["R_mean"].values
yerr = np.maximum(agg["R_sem"].values, 1e-6)

def model_A(theta, t): a,b = theta; return a + b*t
def model_B(theta, t): Rinf,k,R0 = theta; return Rinf*(1 - np.exp(-k*t)) + R0
def model_C(theta, t): Rinf,k,t0 = theta; return Rinf / (1 + np.exp(-k*(t - t0)))

def fit_model(fun, theta0, t, y, yerr, max_iter=800, lr=1e-2):
    w = 1.0/yerr
    theta = np.array(theta0, dtype=float)
    for _ in range(max_iter):
        yhat = fun(theta, t)
        r = (y - yhat)*w
        # numerical jacobian
        J = []
        eps = 1e-6
        for i in range(len(theta)):
            dtheta = np.zeros_like(theta); dtheta[i] = eps
            y2 = fun(theta + dtheta, t)
            J.append(((y2 - yhat)/eps)*w)
        J = np.vstack(J).T
        step, *_ = np.linalg.lstsq(J, r, rcond=None)
        theta += lr*step
        if np.linalg.norm(step) < 1e-6: break
    yhat = fun(theta, t); resid = (y - yhat)/yerr
    rss = float(np.sum(resid**2)); n=len(y); p=len(theta)
    aic = n*np.log(rss/n + 1e-12) + 2*p
    bic = n*np.log(rss/n + 1e-12) + p*np.log(max(n,1))
    return theta, rss, aic, bic

# initial guesses
a0 = y.min(); b0 = (y.max()-y.min())/max(1e-3, x.max()-x.min())
thetaA, rssA, aicA, bicA = fit_model(model_A, [a0, b0], x, y, yerr)
thetaB, rssB, aicB, bicB = fit_model(model_B, [y.max(), 0.2, y.min()], x, y, yerr)
thetaC, rssC, aicC, bicC = fit_model(model_C, [y.max(), 0.2, x.mean()], x, y, yerr)

summary = pd.DataFrame([
    {"model":"A_linear",           "params":thetaA.tolist(), "rss":rssA,"AIC":aicA,"BIC":bicA},
    {"model":"B_saturating_exp",   "params":thetaB.tolist(), "rss":rssB,"AIC":aicB,"BIC":bicB},
    {"model":"C_logistic",         "params":thetaC.tolist(), "rss":rssC,"AIC":aicC,"BIC":bicC},
])

# 6) Plot
t_fit = np.linspace(0, x.max()*1.05, 200)
plt.figure(figsize=(7,5))
plt.errorbar(x, y, yerr=yerr, fmt='o', label="binned data")
plt.plot(t_fit, model_A(thetaA, t_fit), label="A linear")
plt.plot(t_fit, model_B(thetaB, t_fit), label="B saturating exp")
plt.plot(t_fit, model_C(thetaC, t_fit), label="C logistic")
plt.xlabel("Lookback time (Gyr)")
plt.ylabel("Mean coherence index ⟨R⟩")
plt.title("UT26 coherence growth vs cosmic time")
plt.legend()
plt.tight_layout()
plt.savefig(OUT_PNG, dpi=150)

agg.to_csv(OUT_BINS, index=False)
summary.to_csv(OUT_FITS, index=False)
print("Saved:", OUT_PNG, OUT_BINS, OUT_FITS)