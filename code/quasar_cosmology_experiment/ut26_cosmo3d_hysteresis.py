# ut26_cosmo3d_hysteresis.py
import os, json
import numpy as np
import matplotlib.pyplot as plt

try:
    from scipy.ndimage import label
    SCIPY_OK = True
except Exception:
    SCIPY_OK = False

# -------- Defaults (same as your sim) --------
SEED        = 123
N           = 96
SNAP_EVERY  = 50

N_SPECTRAL_BINS = 40
NS_INDEX    = 0.0
K0_CUTOFF   = 0.15
BAO_A       = 0.06
BAO_R       = 105.0
BAO_SIG     = 0.02

BETA        = 3.0
LAMBDA_R    = 0.20
ETA_THRESH  = 0.55
DRIVE_W     = 2*np.pi/30
NOISE_STD   = 0.35
TRACE_COST  = np.log(2.0)

EPS_DRIFT   = 0.08
A_GROW      = 0.9
B_DAMP      = 0.6

DELTA_THR   = 0.15
MASS_MIN    = 20

OUTDIR_BASE = "ut26_cosmo3d_outputs"

# -------- Hysteresis schedule from env --------
# Phase 1: A1 for T1 steps; Phase 2: A2 for T2 steps
PHASE1_A = float(os.getenv("PHASE1_A", 0.90))
PHASE1_T = int(os.getenv("PHASE1_T",  200))
PHASE2_A = float(os.getenv("PHASE2_A", 0.30))
PHASE2_T = int(os.getenv("PHASE2_T",  200))

# Allow env overrides for other params (optional)
BETA        = float(os.getenv("BETA",       BETA))
LAMBDA_R    = float(os.getenv("LAMBDA_R",   LAMBDA_R))
ETA_THRESH  = float(os.getenv("ETA_THRESH", ETA_THRESH))
DRIVE_W     = float(os.getenv("DRIVE_W",    DRIVE_W))
NOISE_STD   = float(os.getenv("NOISE_STD",  NOISE_STD))

RUN_TAG = os.getenv("RUN_TAG", f"hyst_A{PHASE1_A}x{PHASE1_T}_A{PHASE2_A}x{PHASE2_T}")
RUN_TAG = RUN_TAG.strip().replace("\\","_").replace("/","_")
OUTDIR  = os.path.join(OUTDIR_BASE, RUN_TAG)

rng = np.random.default_rng(SEED)

def ensure():
    os.makedirs(OUTDIR, exist_ok=True)

def kgrid(n):
    k = np.fft.fftfreq(n)*n
    kx, ky, kz = np.meshgrid(k, k, k, indexing='ij')
    return np.sqrt(kx**2 + ky**2 + kz**2)

def bao_like_P0(kk):
    P_smooth = (kk + 1e-12)**NS_INDEX * np.exp(-(kk*K0_CUTOFF)**2)
    wiggle   = 1.0 + BAO_A * np.sin(kk * (BAO_R/800.0)) * np.exp(-(kk*BAO_SIG*10.0)**2)
    return P_smooth * wiggle

def gaussian_field_from_P0(n):
    kk  = kgrid(n)
    P0  = bao_like_P0(kk)
    amp = np.sqrt(np.maximum(P0, 0.0)) / np.sqrt(2.0)
    pr  = rng.normal(size=(n,n,n))
    pi  = rng.normal(size=(n,n,n))
    F   = amp * (pr + 1j*pi)
    F[0,0,0] = 0.0
    field = np.fft.ifftn(F).real
    field -= field.mean()
    field /= (field.std() + 1e-12)
    return field

def neighbor_mean_3d(arr):
    up    = np.roll(arr, -1, axis=0)
    down  = np.roll(arr,  1, axis=0)
    left  = np.roll(arr, -1, axis=1)
    right = np.roll(arr,  1, axis=1)
    front = np.roll(arr, -1, axis=2)
    back  = np.roll(arr,  1, axis=2)
    return (up + down + left + right + front + back) / 6.0

def spatial_entropy(s, bins=32):
    hist,_ = np.histogram(s.ravel(), bins=bins, range=(0.0,1.0))
    p = hist.astype(float) / (hist.sum() + 1e-12)
    p = p[p>0]
    return float(-(p*np.log2(p)).sum() / np.log2(bins))

def main():
    ensure()
    T = PHASE1_T + PHASE2_T
    # amplitude schedule A(t)
    A_sched = np.concatenate([np.full(PHASE1_T, PHASE1_A), np.full(PHASE2_T, PHASE2_A)])

    print("UT26 Hysteresis run")
    print(f"T={T} = {PHASE1_T}(A={PHASE1_A}) + {PHASE2_T}(A={PHASE2_A}), W={DRIVE_W}")
    print("OUTDIR:", OUTDIR)

    # Seed bias field b(x)
    raw = gaussian_field_from_P0(N)
    b   = raw / (np.max(np.abs(raw)) + 1e-12)

    # Initial coherence
    s = 0.5 + 0.1*raw
    s = np.clip(s, 0.0, 1.0)

    R_total = 0.0
    prune_count = 0

    # Logs
    times, A_log, mean_s, H_log, prunes_log = [], [], [], [], []

    for t in range(T):
        A = A_sched[t]
        drive_t = A * np.sin(DRIVE_W * t)
        noise   = rng.normal(0.0, NOISE_STD, size=(N,N,N))

        trig = (np.abs(drive_t) + np.abs(noise)) > ETA_THRESH

        if np.any(trig):
            p1 = 1.0 / (1.0 + np.exp(-BETA * b))
            outcome = (rng.random(size=(N,N,N)) < p1).astype(float)
            pruned_local = ((p1 > 0.5) & (outcome < 0.5)) | ((p1 < 0.5) & (outcome > 0.5))
            prune_count += int(pruned_local[trig].sum())
            s[trig]  = outcome[trig]
            R_total += TRACE_COST * float(trig.sum())

        notrig = ~trig
        if np.any(notrig):
            s_nb = neighbor_mean_3d(s)
            s[notrig] = np.clip(s[notrig] + LAMBDA_R*(s_nb[notrig] - s[notrig]), 0.0, 1.0)

        delta_I = s - s.mean()
        dR_dt   = TRACE_COST * trig.astype(float)
        s += EPS_DRIFT * (A_GROW*delta_I - B_DAMP*dR_dt)
        s = np.clip(s, 0.0, 1.0)

        if (t % SNAP_EVERY == 0) or (t == T-1):
            H = spatial_entropy(s, bins=32)
            times.append(t); A_log.append(A); mean_s.append(float(s.mean())); H_log.append(H); prunes_log.append(prune_count)
            print(f"[{t:4d}] A={A:.2f}  <s>={s.mean():.4f}  prunes={prune_count}")

    # Save time series
    import csv
    with open(os.path.join(OUTDIR, "hysteresis.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["t","A","mean_s","prunes"])
        for t, a, ms, pr in zip(times, A_log, mean_s, prunes_log):
            w.writerow([t, a, ms, pr])

    # Summary JSON
    summary = dict(
        N=N, T=T,
        PHASE1_A=PHASE1_A, PHASE1_T=PHASE1_T,
        PHASE2_A=PHASE2_A, PHASE2_T=PHASE2_T,
        BETA=BETA, LAMBDA_R=LAMBDA_R, ETA_THRESH=ETA_THRESH,
        DRIVE_W=DRIVE_W, NOISE_STD=NOISE_STD,
        final_mean_s=float(mean_s[-1]),
        total_prunes=int(prunes_log[-1]),
        OUTDIR=OUTDIR
    )
    with open(os.path.join(OUTDIR,"summary.json"), "w") as f:
        json.dump(summary, f, indent=2)

    print("Wrote:", os.path.join(OUTDIR,"hysteresis.csv"))
    print("Wrote:", os.path.join(OUTDIR,"summary.json"))
    print("Done.")

if __name__ == "__main__":
    os.makedirs(OUTDIR_BASE, exist_ok=True)
    main()