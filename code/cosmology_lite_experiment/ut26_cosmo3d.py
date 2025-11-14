"""
UT26 Cosmology-Lite 3D Simulator (laptop friendly)

- 3D lattice with a UT26 coherence field s(x,t) in [0,1]
- Initial conditions: Gaussian random field with BAO-like wiggles in P0(k)
- UT26 operators per step:
    β  : softmax bias from a static local preference field b(x)
    Γ  : global periodic driver (sinusoid) – "gamma-like" cadence
    λR : return/retention + neighbor coupling (smoothing)
    η* : collapse threshold (drive + noise must exceed to trigger collapse)
- Effective gravity drift:  s += eps*( A*delta_I - B*dR_dt )
- Substrate trace field R(x,t) accumulates Landauer-like entropy per collapse (Lemma)

Observables:
- Power spectrum P(k) of delta_I at final snapshot
- Weak-lensing-like projection (kappa) map and its power spectrum
- Toy halo finder (FoF via connected-component labeling on thresholded delta_I)
- Summary CSVs and PNGs

Run:
    python ut26_cosmo3d.py
"""

import os, json
import numpy as np
import matplotlib.pyplot as plt

try:
    from scipy.ndimage import label
    SCIPY_OK = True
except Exception:
    SCIPY_OK = False

# ----------------------
# Defaults
# ----------------------
SEED        = 123
N           = 96
T           = 300
SNAP_EVERY  = 50

# Initial spectrum (BAO-like)
N_SPECTRAL_BINS = 40
NS_INDEX    = 0.0
K0_CUTOFF   = 0.15
BAO_A       = 0.06
BAO_R       = 105.0
BAO_SIG     = 0.02

# UT26 operators (defaults)
BETA        = 3.0          # β: bias strength
LAMBDA_R    = 0.20         # λR: retention/smoothing
ETA_THRESH  = 0.55         # η*: collapse threshold
DRIVE_A     = 0.65         # Γ amplitude
DRIVE_W     = 2*np.pi/30   # Γ frequency (rad/step)
NOISE_STD   = 0.35         # env noise
TRACE_COST  = np.log(2.0)  # Landauer unit

# Effective drift
EPS_DRIFT   = 0.08
A_GROW      = 0.9
B_DAMP      = 0.6

# Halos (toy)
DELTA_THR   = 0.15
MASS_MIN    = 20

OUTDIR_BASE = "ut26_cosmo3d_outputs"

# ----------------------
# Allow environment overrides (for sweeps)
# ----------------------
BETA        = float(os.getenv("BETA",       BETA))
LAMBDA_R    = float(os.getenv("LAMBDA_R",   LAMBDA_R))
ETA_THRESH  = float(os.getenv("ETA_THRESH", ETA_THRESH))
DRIVE_A     = float(os.getenv("DRIVE_A",    DRIVE_A))
DRIVE_W     = float(os.getenv("DRIVE_W",    DRIVE_W))
NOISE_STD   = float(os.getenv("NOISE_STD",  NOISE_STD))

# Unique output folder per run (sanitise any stray whitespace or slashes)
RUN_TAG = os.getenv(
    "RUN_TAG",
    f"beta{BETA}_lr{LAMBDA_R}_eta{ETA_THRESH}_A{DRIVE_A}_W{DRIVE_W}"
)
RUN_TAG = RUN_TAG.strip().replace("\\", "_").replace("/", "_")
OUTDIR  = os.path.join(OUTDIR_BASE, RUN_TAG)

# ----------------------
# Utilities
# ----------------------
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

def power_spectrum(delta):
    n  = delta.shape[0]
    dk = np.fft.fftn(delta)
    pk3d = (dk*dk.conjugate()).real
    kk = kgrid(n)
    edges = np.linspace(0.0, kk.max(), N_SPECTRAL_BINS+1)
    Pk = np.zeros(N_SPECTRAL_BINS); Nk = np.zeros(N_SPECTRAL_BINS, dtype=int)
    inds = np.digitize(kk.ravel(), edges) - 1
    for i in range(N_SPECTRAL_BINS):
        m = (inds == i)
        Nk[i] = int(m.sum())
        if Nk[i] > 0:
            Pk[i] = pk3d.ravel()[m].mean()
    kmid = 0.5*(edges[:-1] + edges[1:])
    return kmid, Pk

def weak_lensing_kappa(delta):
    kappa = delta.sum(axis=2)
    kappa -= kappa.mean()
    kappa /= (kappa.std() + 1e-12)
    return kappa

def fof_halos(delta_thr_mask):
    if not SCIPY_OK:
        return []
    structure = np.zeros((3,3,3), dtype=int)
    structure[1,1,0] = structure[1,1,2] = 1
    structure[1,0,1] = structure[1,2,1] = 1
    structure[0,1,1] = structure[2,1,1] = 1
    lab, nlab = label(delta_thr_mask, structure)
    sizes = []
    for i in range(1, nlab+1):
        sizes.append(int((lab==i).sum()))
    return sizes

def binary_lz_complexity(bits):
    b = bytes(bits.astype(np.uint8).tolist())
    seen = set(); i = 0; c = 0; n = len(b)
    while i < n:
        j = i+1
        while j <= n and b[i:j] in seen:
            j += 1
        seen.add(b[i:j]); c += 1; i = j
    if n < 2: return float(n)
    return c / (n / np.log(n + 1))

def spatial_entropy(s, bins=32):
    hist,_ = np.histogram(s.ravel(), bins=bins, range=(0.0,1.0))
    p = hist.astype(float) / (hist.sum() + 1e-12)
    p = p[p>0]
    return float(-(p*np.log2(p)).sum() / np.log2(bins))

# ----------------------
# Main
# ----------------------
def main():
    ensure()
    print("UT26 Cosmology-Lite 3D simulator")
    print(f"N={N}, T={T}, output -> {OUTDIR}")
    print("Parameters this run:")
    print("  BETA      =", BETA)
    print("  LAMBDA_R  =", LAMBDA_R)
    print("  ETA_THRESH=", ETA_THRESH)
    print("  DRIVE_A   =", DRIVE_A)
    print("  DRIVE_W   =", DRIVE_W)
    print("  NOISE_STD =", NOISE_STD)

    # Seed bias field b(x) from initial Gaussian field (smoothed, normalized to [-1,1])
    raw = gaussian_field_from_P0(N)
    b   = raw / (np.max(np.abs(raw)) + 1e-12)

    # Initial coherence s in [0,1]
    s = 0.5 + 0.1*raw
    s = np.clip(s, 0.0, 1.0)

    # Substrate trace & loggers
    R = np.zeros_like(s)
    R_total = 0.0
    times, mean_s, H_log, C_log, prunes_log = [], [], [], [], []
    prune_count = 0

    for t in range(T):
        # Γ driver + noise
        drive_t = DRIVE_A * np.sin(DRIVE_W * t)
        noise   = rng.normal(0.0, NOISE_STD, size=(N,N,N))

        # collapse mask
        trig = (np.abs(drive_t) + np.abs(noise)) > ETA_THRESH

        if np.any(trig):
            # collapse via β-softmax
            p1 = 1.0 / (1.0 + np.exp(-BETA * b))
            outcome = (rng.random(size=(N,N,N)) < p1).astype(float)

            pruned_local = ((p1 > 0.5) & (outcome < 0.5)) | ((p1 < 0.5) & (outcome > 0.5))
            prune_count += int(pruned_local[trig].sum())

            s[trig]  = outcome[trig]
            R[trig] += TRACE_COST
            R_total += TRACE_COST * float(trig.sum())

        # return: neighbor coupling (λR)
        notrig = ~trig
        if np.any(notrig):
            s_nb = neighbor_mean_3d(s)
            s[notrig] = np.clip(s[notrig] + LAMBDA_R*(s_nb[notrig] - s[notrig]), 0.0, 1.0)

        # effective drift
        delta_I = s - s.mean()
        dR_dt   = TRACE_COST * trig.astype(float)
        s += EPS_DRIFT * (A_GROW*delta_I - B_DAMP*dR_dt)
        s = np.clip(s, 0.0, 1.0)

        # record
        if (t % SNAP_EVERY == 0) or (t == T-1):
            H = spatial_entropy(s, bins=32)
            bits = (s.ravel() > 0.5).astype(int)
            C = binary_lz_complexity(bits)
            times.append(t); mean_s.append(float(s.mean()))
            H_log.append(H); C_log.append(C); prunes_log.append(prune_count)
            print(f"[{t:4d}] mean s={s.mean():.3f}  R_total={R_total:.1f}  pruned={prune_count}")

    # ----- Final observables -----
    delta = s - s.mean()

    # P(k)
    k_mid, Pk = power_spectrum(delta)
    np.savetxt(os.path.join(OUTDIR,"pk.csv"), np.c_[k_mid, Pk],
               delimiter=",", header="k,Pk", comments="")

    # kappa map + spectrum
    kappa = weak_lensing_kappa(delta)
    plt.figure(figsize=(5,4))
    plt.imshow(kappa.T, origin="lower", cmap="viridis")
    plt.colorbar(label="kappa (proj. delta)")
    plt.title("Weak-lensing-like κ (projection)")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTDIR,"kappa_map.png"), dpi=140)
    plt.close()

    ky = np.fft.fftfreq(kappa.shape[0])*kappa.shape[0]
    kx = np.fft.fftfreq(kappa.shape[1])*kappa.shape[1]
    KX, KY = np.meshgrid(kx, ky, indexing="ij")
    K = np.sqrt(KX**2 + KY**2)
    edges = np.linspace(0, K.max(), 30+1)
    FTk = np.fft.fft2(kappa)
    PS2 = (FTk*FTk.conjugate()).real
    P2 = np.zeros(30); N2 = np.zeros(30, dtype=int)
    idx = np.digitize(K.ravel(), edges) - 1
    for i in range(30):
        m = (idx == i)
        N2[i] = int(m.sum())
        if N2[i] > 0: P2[i] = PS2.ravel()[m].mean()
    km2 = 0.5*(edges[:-1]+edges[1:])
    np.savetxt(os.path.join(OUTDIR,"kappa_ps.csv"), np.c_[km2,P2],
               delimiter=",", header="k,Pkappa", comments="")
    plt.figure(figsize=(5,4))
    plt.plot(km2, P2, lw=1.7)
    plt.xlabel("k (2D)"); plt.ylabel("P_kappa")
    plt.title("κ power spectrum (toy)")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTDIR,"kappa_ps.png"), dpi=140)
    plt.close()

    # HMF (toy FoF)
    if SCIPY_OK:
        msk = (delta > DELTA_THR)
        sizes = [sz for sz in fof_halos(msk) if sz >= MASS_MIN]
        if sizes:
            bins = np.logspace(np.log10(MASS_MIN), np.log10(max(sizes)), 16)
            hist, edges = np.histogram(sizes, bins=bins)
            centers = np.sqrt(edges[:-1]*edges[1:])
            np.savetxt(os.path.join(OUTDIR,"hmf.csv"), np.c_[centers, hist],
                       delimiter=",", header="mass,counts", comments="")
            plt.figure(figsize=(5,4))
            plt.loglog(centers, np.maximum(hist,1e-6), marker='o')
            plt.xlabel("halo cell count (proxy mass)")
            plt.ylabel("counts"); plt.title("Toy HMF (connected components)")
            plt.grid(alpha=0.3, which="both")
            plt.tight_layout()
            plt.savefig(os.path.join(OUTDIR,"hmf.png"), dpi=140)
            plt.close()

    # summary triptych
    plt.figure(figsize=(12,4))
    plt.subplot(1,3,1)
    plt.plot(times, mean_s, lw=1.7); plt.grid(alpha=0.3)
    plt.xlabel("time"); plt.ylabel("<s>"); plt.title("Mean coherence (saturation)")

    plt.subplot(1,3,2)
    plt.plot(times, H_log, label="H"); plt.plot(times, C_log, label="C"); plt.grid(alpha=0.3)
    plt.xlabel("time"); plt.title("H, C over time"); plt.legend()

    plt.subplot(1,3,3)
    plt.plot(times, prunes_log, lw=1.7); plt.grid(alpha=0.3)
    plt.xlabel("time"); plt.ylabel("cumulative prunes"); plt.title("Lawful pruning")

    plt.tight_layout()
    plt.savefig(os.path.join(OUTDIR,"summary.png"), dpi=150)
    plt.close()

    # summary JSON (with parameters logged)
    summary = dict(
        N=N, T=T, seed=SEED,
        BETA=BETA, LAMBDA_R=LAMBDA_R, ETA_THRESH=ETA_THRESH,
        DRIVE_A=DRIVE_A, DRIVE_W=DRIVE_W, NOISE_STD=NOISE_STD,
        final_mean_s=float(mean_s[-1]),
        total_trace_R=float(R_total),
        total_prunes=int(prune_count),
        SCIPY_OK=SCIPY_OK,
        OUTDIR=OUTDIR
    )
    with open(os.path.join(OUTDIR,"summary.json"), "w") as f:
        json.dump(summary, f, indent=2)

    print("\n=== Done ===")
    print("Outputs in:", OUTDIR)
    print(" - pk.csv, kappa_map.png, kappa_ps.png, hmf.csv (if scipy available)")
    print(" - summary.png, summary.json")

# ----------------------
if __name__ == "__main__":
    ensure()
    main()