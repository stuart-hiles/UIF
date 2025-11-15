# ut26_quasar_full_run_v4.py
import os, tarfile, argparse, gzip
import numpy as np, pandas as pd
from scipy.signal import lombscargle

def open_text_maybe_gz(path):
    if path.lower().endswith(".gz"):
        try:
            return gzip.open(path, "rt", encoding="utf-8", errors="ignore")
        except Exception:
            pass
    return open(path, "r", encoding="utf-8", errors="ignore")

def spectral_entropy_lomb(mjd, mag, restframe=True, z=None,
                          fmin=1/5000, fmax=1, nfreq=1024):
    if len(mjd) < 10:
        return np.nan
    t = mjd - mjd.min()
    if restframe and z and z > 0:
        t = t / (1 + z)
    x = mag - np.median(mag)
    freqs = np.logspace(np.log10(fmin), np.log10(fmax), nfreq)
    w = 2*np.pi*freqs
    P = lombscargle(t, x, w, normalize=True)
    P = np.maximum(P, 1e-12)
    P = P / P.sum()
    return float(-(P * np.log2(P)).sum() / np.log2(len(P)))

def lz_complexity_quantised(mag):
    if len(mag) < 10:
        return np.nan
    x = mag - np.median(mag)
    dx = np.diff(x)
    rng = np.ptp(dx)  # NumPy 2.0-safe
    q = np.clip(((dx - dx.min()) / (rng + 1e-12) * 255).astype(np.uint8), 0, 255)
    s = bytes(q.tolist())
    # Simple LZ76 scan
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

def extract_i_band(lines):
    mjd, mag, err = [], [], []
    bad = 0
    for ln in lines:
        p = ln.split()
        if len(p) < 17:
            bad += 1; continue
        try:
            mjd_i, mag_i, err_i = float(p[9]), float(p[10]), float(p[11])
        except Exception:
            bad += 1; continue
        if mag_i <= -99 or err_i <= 0 or mjd_i <= 0:
            bad += 1; continue
        mjd.append(mjd_i); mag.append(mag_i); err.append(err_i)
    return np.array(mjd), np.array(mag), np.array(err), bad

def load_db_table(db_path):
    rows = []
    with open_text_maybe_gz(db_path) as f:
        for ln in f:
            if ln.startswith("#") or not ln.strip(): continue
            toks = ln.split()
            if len(toks) < 15: continue
            try:
                dbid = int(toks[0]); z = float(toks[6]); iMag = float(toks[-3])
            except Exception:
                continue
            rows.append((dbid, z, iMag))
    return pd.DataFrame(rows, columns=["dbID","z","iMag"])

def run_full(tar_path, db_path, out_dir, max_objs=None):
    os.makedirs(out_dir, exist_ok=True)
    print("[info] cwd:", os.getcwd())
    print("[info] DB:", db_path)
    print("[info] TAR:", tar_path)

    db = load_db_table(db_path)
    print(f"[info] DB rows loaded: {len(db)}")
    if db.empty:
        print("[error] Empty DB — stopping.")
        pd.DataFrame([]).to_csv(os.path.join(out_dir, "quasar_raw_HC_all.csv"), index=False)
        return

    try:
        tar = tarfile.open(tar_path, "r:*")  # transparent compression
    except tarfile.ReadError as e:
        print("[error] Could not open tar:", e)
        pd.DataFrame([]).to_csv(os.path.join(out_dir, "quasar_raw_HC_all.csv"), index=False)
        return

    out_rows = []
    total_members = matched_ids = enough_points = processed = 0
    errors = 0

    for member in tar:
        if not member.isfile(): continue
        total_members += 1
        name = member.name.replace("\\", "/")
        if not name.startswith("QSO_S82/"): continue
        base = os.path.basename(name)
        try:
            dbid = int(base)
        except Exception:
            continue

        meta = db.loc[db["dbID"] == dbid]
        if meta.empty: continue
        matched_ids += 1
        z = float(meta["z"].values[0]); iMag = float(meta["iMag"].values[0])

        try:
            f = tar.extractfile(member)
            if f is None: continue
            lines = f.read().decode("utf-8","ignore").splitlines()
            mjd, mag, err, bad = extract_i_band(lines)
            if len(mag) < 10: continue
            enough_points += 1

            H = spectral_entropy_lomb(mjd, mag, restframe=True, z=z)
            C = lz_complexity_quantised(mag)
            out_rows.append({"dbID":dbid,"z":z,"iMag":iMag,"npts":len(mag),"H":H,"C":C})
            processed += 1

            if processed % 50 == 0:
                print(f"[info] processed={processed} matched={matched_ids} >=10pt={enough_points} members={total_members} rows={len(out_rows)}")

            if max_objs and processed >= max_objs:
                break

        except Exception as e:
            errors += 1
            print(f"[warn] dbID={dbid}: {e}")

    tar.close()

    out_path = os.path.join(out_dir, "quasar_raw_HC_all.csv")
    pd.DataFrame(out_rows).to_csv(out_path, index=False)
    print("[done] Wrote:", out_path)
    print(f"[stats] total tar members: {total_members}")
    print(f"[stats] matched dbIDs:     {matched_ids}")
    print(f"[stats] >=10 i-band pts:   {enough_points}")
    print(f"[stats] rows written:      {len(out_rows)}")
    print(f"[stats] errors:            {errors}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="UT26 Raw Quasar H–C Full Run (verbose)")
    parser.add_argument("--tar", type=str, required=True, help="QSO_S82.tar or .tar.gz")
    parser.add_argument("--db",  type=str, required=True, help="DB_QSO_S82.dat or .dat.gz")
    parser.add_argument("--out", type=str, default="ut26_out")
    parser.add_argument("--max", type=int, default=None)
    args = parser.parse_args()
    run_full(args.tar, args.db, args.out, args.max)