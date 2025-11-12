# UT26 EEG Pipeline (recursive, ROI + band-limited H & C)
# - Recursively loads EDF/FIF from data/** (e.g., data/S001/S001R01.edf)
# - Preprocess -> windows -> H (band-limited spectral entropy), C (band-limited LZ on delta)
# - Builds surrogates (shuffle + phase) with the same band-limit and ROI
# - Saves CSVs and an H–C plane figure

import os, glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import welch, butter, filtfilt
from numpy.fft import rfft, irfft
from tqdm import tqdm
import mne

# ----------------------------
# CONFIG
# ----------------------------
DATADIR = "data"       # folders like data/S001/S001R01.edf
OUTDIR  = "outputs"

# Filters & windows
WIN_SEC  = 4.0
STEP_SEC = 2.0
BP_LO, BP_HI = 1.0, 45.0
NOTCH = [50.0, 60.0]
FS_FALLBACK = 128.0

# Entropy band (set to alpha or gamma as needed)
# ENTROPY_BAND = (8.0, 12.0)    # alpha
ENTROPY_BAND = (8.0, 12.0)

# ROI channels (posterior/occipital)
ROI = ["O1","O2","Oz","POz","PO3","PO4","Pz","P3","P4"]

# ----------------------------
# UTILITIES
# ----------------------------
def ensure_dirs():
    os.makedirs(DATADIR, exist_ok=True)
    os.makedirs(OUTDIR,  exist_ok=True)

def infer_state_from_run(base_name: str) -> str:
    if "R01" in base_name: return "eyes_open"
    if "R02" in base_name: return "eyes_closed"
    return "task"

def make_windows(n_samples, sf, win_s=WIN_SEC, step_s=STEP_SEC):
    w = int(win_s * sf)
    step = int(step_s * sf)
    return [(i, i + w) for i in range(0, max(0, n_samples - w + 1), step)]

def spectral_entropy_band(x, sf, band):
    f, P = welch(x, fs=sf, nperseg=min(1024, len(x)))
    mask = (f >= band[0]) & (f <= band[1])
    if not np.any(mask): return np.nan
    Pband = np.maximum(P[mask], 1e-12)
    Pband = Pband / (Pband.sum() + 1e-12)
    H = -(Pband * np.log2(Pband)).sum() / np.log2(len(Pband))
    return float(H)

def lz_complexity_delta(x):
    if len(x) < 10: return np.nan
    dx = np.diff(x)
    rng = np.ptp(dx)
    q = np.clip(((dx - dx.min()) / (rng + 1e-12) * 255).astype(np.uint8), 0, 255)
    b = bytes(q.tolist())
    seen = set(); i = 0; c = 0; n = len(b)
    while i < n:
        j = i+1
        while j <= n and b[i:j] in seen:
            j += 1
        seen.add(b[i:j]); c += 1; i = j
    if n < 2: return float(n)
    return c / (n / np.log(n + 1))

def phase_randomise_uniform(x):
    X = rfft(x - x.mean())
    phases = np.exp(1j * np.random.uniform(0, 2*np.pi, size=X.shape))
    phases[0] = 1.0
    xr = irfft(np.abs(X) * phases, n=len(x))
    xr = xr / (np.std(xr) + 1e-12) * (np.std(x) + 1e-12) + x.mean()
    return xr

def report_local_files():
    print("[1/5] Using local EDF/FIF files in:", os.path.abspath(DATADIR))
    fifs = glob.glob(os.path.join(DATADIR, "**", "*.fif"), recursive=True)
    edfs = glob.glob(os.path.join(DATADIR, "**", "*.edf"), recursive=True)
    found = fifs + edfs
    if not found:
        print("  No EDF/FIF found. Place files like S001/S001R01.edf under", DATADIR)
    else:
        for p in (found[:8]):
            print("  found:", os.path.relpath(p, DATADIR))

# ----------------------------
# STEP 2/3: REAL WINDOWS -> H, C, R
# ----------------------------
def process_records():
    print("[2/5] Preprocess and window -> H, C, R ...")
    rows = []

    fifs = glob.glob(os.path.join(DATADIR, "**", "*.fif"), recursive=True)
    edfs = glob.glob(os.path.join(DATADIR, "**", "*.edf"), recursive=True)
    files = fifs if fifs else edfs
    if not files:
        print("  No .edf/.fif files found. Did you copy the EDFs into data/?")
        return pd.DataFrame([])

    for fpath in tqdm(files):
        basefile = os.path.basename(fpath)
        base = basefile.replace(".fif","").replace(".edf","")
        state = infer_state_from_run(base)

        try:
            if fpath.lower().endswith(".fif"):
                raw = mne.io.read_raw_fif(fpath, preload=True, verbose=False)
            else:
                raw = mne.io.read_raw_edf(fpath, preload=True, verbose=False)
        except Exception as e:
            print("  read-fail:", basefile, e); continue

        # Preprocessing
        try:
            raw.filter(BP_LO, BP_HI, fir_design="firwin", verbose=False)
            raw.notch_filter(NOTCH, verbose=False)
            raw.set_eeg_reference("average", verbose=False)
        except Exception as e:
            print("  filter-warn:", basefile, e)

        sf = raw.info.get("sfreq") or FS_FALLBACK

        # --- ROI selection ---
        picks = [i for i, ch in enumerate(raw.ch_names)
                 if any(ch.upper().startswith(r.upper()) for r in ROI)]
        if len(picks) >= 2:
            print("Using ROI:", [raw.ch_names[i] for i in picks])
            data = raw.get_data(picks=picks)
        else:
            data = raw.get_data()

        idx  = make_windows(data.shape[1], sf)

        # Bandpass for C as well
        b, a = butter(3, [ENTROPY_BAND[0]/(sf/2), ENTROPY_BAND[1]/(sf/2)], btype="band")

        for (a0, a1) in idx:
            seg = data[:, a0:a1]
            Hs, Cs = [], []
            for ch in seg:
                try:
                    ch_band = filtfilt(b, a, ch)
                except Exception:
                    ch_band = ch
                h = spectral_entropy_band(ch_band, sf, band=ENTROPY_BAND)
                c = lz_complexity_delta(ch_band)
                if not np.isnan(h): Hs.append(h)
                if not np.isnan(c): Cs.append(c)
            if Hs and Cs:
                H = float(np.mean(Hs)); C = float(np.mean(Cs))
                rows.append({"rec": base, "win": a0, "state": state, "H": H, "C": C})

    df = pd.DataFrame(rows)
    if df.empty:
        print("  No windows processed.")
        return df

    # Normalize C within recording; compute R
    def norm_minmax(s):
        mn, mx = s.min(), s.max()
        if mx - mn < 1e-12: return np.zeros_like(s, dtype=float)
        return (s - mn) / (mx - mn)

    df["C_norm"] = df.groupby("rec")["C"].transform(norm_minmax)
    df["R"] = (1.0 - df["H"]) + df["C_norm"]

    out = os.path.join(OUTDIR, "EEG_windows_HCR.csv")
    df.to_csv(out, index=False)
    print("  wrote:", out)
    return df

# ----------------------------
# STEP 4: SURROGATES
# ----------------------------
def build_surrogates():
    print("[3/5] Building surrogates (shuffle + phase) ...")
    rows = []

    fifs = glob.glob(os.path.join(DATADIR, "**", "*.fif"), recursive=True)
    edfs = glob.glob(os.path.join(DATADIR, "**", "*.edf"), recursive=True)
    files = fifs if fifs else edfs

    for fpath in tqdm(files):
        basefile = os.path.basename(fpath)
        base = basefile.replace(".fif","").replace(".edf","")

        try:
            if fpath.lower().endswith(".fif"):
                raw = mne.io.read_raw_fif(fpath, preload=True, verbose=False)
            else:
                raw = mne.io.read_raw_edf(fpath, preload=True, verbose=False)
        except Exception:
            continue

        try:
            raw.filter(BP_LO, BP_HI, fir_design="firwin", verbose=False)
            raw.notch_filter(NOTCH, verbose=False)
            raw.set_eeg_reference("average", verbose=False)
        except Exception:
            pass

        sf = raw.info.get("sfreq") or FS_FALLBACK

        # ROI selection for surrogates
        picks = [i for i, ch in enumerate(raw.ch_names)
                 if any(ch.upper().startswith(r.upper()) for r in ROI)]
        if len(picks) >= 2:
            data = raw.get_data(picks=picks)
        else:
            data = raw.get_data()

        idx  = make_windows(data.shape[1], sf)
        b, a = butter(3, [ENTROPY_BAND[0]/(sf/2), ENTROPY_BAND[1]/(sf/2)], btype="band")

        for (a0, a1) in idx:
            seg = data[:, a0:a1]
            for kind in ("shuffle","phase"):
                Hs, Cs = [], []
                for ch in seg:
                    if kind == "shuffle":
                        xx = ch.copy(); np.random.shuffle(xx)
                    else:
                        xx = phase_randomise_uniform(ch)
                    try:
                        xx_band = filtfilt(b, a, xx)
                    except Exception:
                        xx_band = xx
                    h = spectral_entropy_band(xx_band, sf, band=ENTROPY_BAND)
                    c = lz_complexity_delta(xx_band)
                    if not np.isnan(h): Hs.append(h)
                    if not np.isnan(c): Cs.append(c)
                if Hs and Cs:
                    rows.append({"rec": base, "win": a0, "kind": kind,
                                 "H": float(np.mean(Hs)), "C": float(np.mean(Cs))})

    dfs = pd.DataFrame(rows)
    out = os.path.join(OUTDIR, "EEG_surrogates_HCR.csv")
    dfs.to_csv(out, index=False)
    print("  wrote:", out)
    return dfs

# ----------------------------
# STEP 5: FIGURES & SUMMARY
# ----------------------------
def make_figures(df, dfs):
    print("[4/5] Making figures + summaries ...")
    if df.empty:
        print("  No real windows; skipping plots.")
        return
    plt.figure(figsize=(6,6))
    for st, sub in df.groupby("state"):
        plt.scatter(1 - sub["H"], sub["C"], s=6, alpha=0.6, label=st)
    if not dfs.empty:
        plt.scatter(1 - dfs["H"], dfs["C"], s=3, alpha=0.3, label="surrogates", color="grey")
    plt.xlabel("1 - H (band-limited entropy)")
    plt.ylabel("C (band-limited LZ on delta)")
    plt.title("EEG complexity–entropy plane (real vs surrogates)")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    fig_path = os.path.join(OUTDIR, "Fig_EEG_HC_plane.png")
    plt.savefig(fig_path, dpi=150)
    plt.close()
    print("  wrote:", fig_path)

    summ = df.groupby("state")["R"].agg(["mean","std","count"])
    summ.to_csv(os.path.join(OUTDIR, "EEG_state_summary_R.csv"))
    print("  wrote:", os.path.join(OUTDIR, "EEG_state_summary_R.csv"))
    print(summ)

def main():
    ensure_dirs()
    print("UT26 EEG pipeline starting ...")
    report_local_files()
    df  = process_records()
    dfs = build_surrogates()
    make_figures(df, dfs)
    print("[5/5] Done.")

if __name__ == "__main__":
    main()