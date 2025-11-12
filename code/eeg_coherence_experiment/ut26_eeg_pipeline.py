# ut26_eeg_pipeline.py
import os, glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from scipy.signal import welch
from numpy.fft import rfft, irfft
import mne
from tqdm import tqdm

# ------------------------------------------------------------
# CONFIG
# ------------------------------------------------------------
DATADIR = "data"      # put your EDF/FIF files here (e.g., data\S001R01.edf)
OUTDIR  = "outputs"

# Windowing / filters
WIN_SEC  = 4.0
STEP_SEC = 2.0
BP_LO, BP_HI = 1.0, 45.0
NOTCH = [50.0, 60.0]
FS_FALLBACK = 128.0

# Spectral entropy band (alpha by default)
ENTROPY_BAND = (8.0, 12.0)  # Hz; change to (30,45) for gamma, etc.

# ------------------------------------------------------------
# UTILITIES
# ------------------------------------------------------------
def ensure_dirs():
    os.makedirs(DATADIR, exist_ok=True)
    os.makedirs(OUTDIR,  exist_ok=True)

def infer_state_from_run(base_name):
    """
    Map run IDs to coarse states:
      R01 -> eyes_open
      R02 -> eyes_closed
      else -> task
    """
    if "R01" in base_name: return "eyes_open"
    if "R02" in base_name: return "eyes_closed"
    return "task"

def make_windows(n_samples, sf, win_s=WIN_SEC, step_s=STEP_SEC):
    w = int(win_s * sf)
    step = int(step_s * sf)
    return [(i, i + w) for i in range(0, max(0, n_samples - w + 1), step)]

def spectral_entropy_band(x, sf, band=ENTROPY_BAND):
    """
    Normalised spectral entropy within a frequency band.
    """
    f, P = welch(x, fs=sf, nperseg=min(1024, len(x)))
    mask = (f >= band[0]) & (f <= band[1])
    # guard if band has no bins
    if not np.any(mask):
        return np.nan
    P = P[mask]
    P = np.maximum(P, 1e-12)
    P /= P.sum()
    H = -(P * np.log2(P)).sum() / np.log2(len(P))
    return float(H)

def lz_complexity_delta(x):
    """
    Lempel-Ziv complexity of the first-difference signal (quantised to 256).
    NumPy 2.0-safe range via np.ptp.
    """
    if len(x) < 10:
        return np.nan
    dx = np.diff(x)
    rng = np.ptp(dx)
    q = np.clip(((dx - dx.min()) / (rng + 1e-12) * 255).astype(np.uint8), 0, 255)
    s = bytes(q.tolist())
    # Simple LZ scan
    i = 0; c = 1; k = 1; n = len(s)
    if n < 2:
        return float(n)
    while True:
        if i + k > n:
            c += 1; break
        sub = s[i:i+k]
        if s.find(sub, 0, i) != -1:
            k += 1
            if i + k > n:
                c += 1; break
        else:
            c += 1
            i += k
            k = 1
        if i == n:
            break
    return float(c) / (n / np.log(n + 1))

def phase_randomise_uniform(x):
    """
    Phase-randomise a 1D signal via FFT, approximately preserving the power spectrum.
    """
    X = rfft(x - x.mean())
    phases = np.exp(1j * np.random.uniform(0, 2*np.pi, size=X.shape))
    phases[0] = 1.0  # preserve DC
    xr = irfft(np.abs(X) * phases, n=len(x))
    xr = xr / (np.std(xr) + 1e-12) * (np.std(x) + 1e-12) + x.mean()
    return xr

def summarize_states_R(df):
    if df.empty:
        return pd.DataFrame(columns=["state","mean","std","count"])
    summ = df.groupby("state")["R"].agg(["mean","std","count"]).reset_index()
    return summ

# ------------------------------------------------------------
# STEP 1: REPORT LOCAL FILES (no download)
# ------------------------------------------------------------
def report_local_files():
    print("[1/5] Using local EDF/FIF files in:", os.path.abspath(DATADIR))
    fifs = glob.glob(os.path.join(DATADIR, "*.fif"))
    edfs = glob.glob(os.path.join(DATADIR, "*.edf"))
    if not (fifs or edfs):
        print("  No EDF/FIF found. Place files like S001R01.edf into", DATADIR)
    else:
        # Show a few examples
        for p in (fifs[:6] or edfs[:6]):
            print("  found:", os.path.basename(p))

# ------------------------------------------------------------
# STEP 2/3: PREPROCESS -> WINDOWS -> H, C, R (per-channel -> averaged)
# ------------------------------------------------------------
def process_records():
    print("[2/5] Preprocess and window -> H, C, R ...")
    rows = []

    # prefer FIF (if pre-saved), else EDF directly
    fif_files = glob.glob(os.path.join(DATADIR, "*.fif"))
    edf_files = glob.glob(os.path.join(DATADIR, "*.edf"))
    files = fif_files if fif_files else edf_files

    if not files:
        print("  No .edf/.fif files found. Did you copy the EDFs into data/?")
        return pd.DataFrame([])

    for fpath in tqdm(files):
        basefile = os.path.basename(fpath)
        base = basefile.replace(".fif","").replace(".edf","")
        state = infer_state_from_run(base)

        # Read either format
        try:
            if fpath.lower().endswith(".fif"):
                raw = mne.io.read_raw_fif(fpath, preload=True, verbose=False)
            else:
                raw = mne.io.read_raw_edf(fpath, preload=True, verbose=False)
        except Exception as e:
            print("  read-fail:", basefile, e)
            continue

        # Basic preprocessing
        try:
            raw.filter(BP_LO, BP_HI, fir_design="firwin", verbose=False)
            raw.notch_filter(NOTCH, verbose=False)
            raw.set_eeg_reference("average", verbose=False)
        except Exception as e:
            print("  filter-warn:", basefile, e)

        sf = raw.info.get("sfreq") or FS_FALLBACK
        data = raw.get_data()  # channels x time
        idx  = make_windows(data.shape[1], sf)

        for w,(a,b) in enumerate(idx):
            seg = data[:, a:b]          # ch x samples
            Hs, Cs = [], []
            for ch in seg:
                h = spectral_entropy_band(ch, sf, band=ENTROPY_BAND)
                c = lz_complexity_delta(ch)
                if not np.isnan(h): Hs.append(h)
                if not np.isnan(c): Cs.append(c)
            if not Hs or not Cs:
                continue
            H = float(np.mean(Hs))
            C = float(np.mean(Cs))
            rows.append({"rec": base, "win": w, "state": state, "H": H, "C": C})

    df = pd.DataFrame(rows)
    if df.empty:
        print("  No windows processed.")
        return df

    # Normalise C within recording; compute R
    # Guard against constant C within a recording
    def norm_minmax(s):
        mn, mx = s.min(), s.max()
        if mx - mn < 1e-12:
            return np.zeros_like(s, dtype=float)
        return (s - mn) / (mx - mn)

    df["C_norm"] = df.groupby("rec")["C"].transform(norm_minmax)
    df["R"] = (1.0 - df["H"]) + df["C_norm"]

    out = os.path.join(OUTDIR, "EEG_windows_HCR.csv")
    df.to_csv(out, index=False)
    print("  wrote:", out)
    return df

# ------------------------------------------------------------
# STEP 4: SURROGATES (shuffle + phase), per-channel -> averaged
# ------------------------------------------------------------
def build_surrogates():
    print("[3/5] Building surrogates (shuffle + phase) ...")
    rows = []

    fif_files = glob.glob(os.path.join(DATADIR, "*.fif"))
    edf_files = glob.glob(os.path.join(DATADIR, "*.edf"))
    files = fif_files if fif_files else edf_files

    for fpath in tqdm(files):
        basefile = os.path.basename(fpath)
        base = basefile.replace(".fif","").replace(".edf","")

        # Read either format
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
        data = raw.get_data()
        idx  = make_windows(data.shape[1], sf)

        for w,(a,b) in enumerate(idx):
            seg = data[:, a:b]          # ch x samples

            # Build two surrogates per channel, then average metrics
            for kind in ("shuffle","phase"):
                Hs, Cs = [], []
                for ch in seg:
                    if kind == "shuffle":
                        xx = ch.copy(); np.random.shuffle(xx)
                    else:
                        xx = phase_randomise_uniform(ch)
                    h = spectral_entropy_band(xx, sf, band=ENTROPY_BAND)
                    c = lz_complexity_delta(xx)
                    if not np.isnan(h): Hs.append(h)
                    if not np.isnan(c): Cs.append(c)
                if not Hs or not Cs:
                    continue
                H = float(np.mean(Hs))
                C = float(np.mean(Cs))
                rows.append({"rec": base, "win": w, "kind": kind, "H": H, "C": C})

    dfs = pd.DataFrame(rows)
    out = os.path.join(OUTDIR, "EEG_surrogates_HCR.csv")
    dfs.to_csv(out, index=False)
    print("  wrote:", out)
    return dfs

# ------------------------------------------------------------
# STEP 5: FIGURES + SUMMARY
# ------------------------------------------------------------
def make_figures(df, dfs):
    print("[4/5] Making figures + summaries ...")
    if df.empty:
        print("  No real windows; skipping plots.")
        return

    # Fig: H–C plane (real states vs surrogates)
    plt.figure(figsize=(6,6))
    for st, sub in df.groupby("state"):
        plt.scatter(1 - sub["H"], sub["C"], s=6, alpha=0.6, label=st)
    if not dfs.empty:
        plt.scatter(1 - dfs["H"], dfs["C"], s=4, alpha=0.3, label="surrogates", color="grey")
    plt.xlabel("1 - H (order)  [band-limited entropy]")
    plt.ylabel("C (LZ on delta signal)")
    plt.title("EEG complexity–entropy plane (real vs surrogates)")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    fig_path = os.path.join(OUTDIR, "Fig_EEG_HC_plane.png")
    plt.savefig(fig_path, dpi=150)
    plt.close()
    print("  wrote:", fig_path)

    # Summary by state (mean R)
    summ = summarize_states_R(df)
    summ.to_csv(os.path.join(OUTDIR, "EEG_state_summary_R.csv"), index=False)
    print("  wrote:", os.path.join(OUTDIR, "EEG_state_summary_R.csv"))
    print(summ)

# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------
def main():
    ensure_dirs()
    print("UT26 EEG pipeline starting ...")

    # Step 1: just report what we have locally
    report_local_files()

    # Steps 2/3: preprocess -> windows -> H,C,R
    df  = process_records()

    # Step 4: surrogates
    dfs = build_surrogates()

    # Step 5: figures + summaries
    make_figures(df, dfs)

    print("[5/5] Done.")

if __name__ == "__main__":
    main()