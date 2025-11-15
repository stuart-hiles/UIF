import os, tarfile, gzip
import numpy as np, pandas as pd

TAR = r"QSO_S82.tar.gz"
DB  = r"DB_QSO_S82.dat"   # use .dat.gz if that's what you have

def open_text_maybe_gz(path):
    if path.lower().endswith(".gz"):
        try:
            return gzip.open(path, "rt", encoding="utf-8", errors="ignore")
        except Exception:
            pass
    return open(path, "r", encoding="utf-8", errors="ignore")

def load_db_ids(db_path, limit=5):
    ids=[]
    with open_text_maybe_gz(db_path) as f:
        for ln in f:
            if ln.startswith("#") or not ln.strip(): continue
            toks = ln.split()
            try:
                dbid = int(toks[0])
            except:
                continue
            ids.append(dbid)
            if len(ids)>=limit: break
    return ids

def extract_i_triplet_tokens(line):
    p = line.split()
    return len(p), p[:18]  # show first ~18 tokens

def extract_i_band(lines):
    # our assumed mapping: u(0..2), g(3..5), r(6..8), i(9..11), z(12..14), RA, Dec
    # i-band triplet at indices [9],[10],[11]
    mjd, mag, err = [], [], []
    bad = 0
    for ln in lines:
        p = ln.split()
        if len(p) < 17:
            bad += 1
            continue
        try:
            mjd_i, mag_i, err_i = float(p[9]), float(p[10]), float(p[11])
        except:
            bad += 1
            continue
        if mag_i <= -99 or err_i <= 0 or mjd_i <= 0:
            bad += 1
            continue
        mjd.append(mjd_i); mag.append(mag_i); err.append(err_i)
    return np.array(mjd), np.array(mag), np.array(err), bad

def main():
    print("[probe] cwd:", os.getcwd())
    print("[probe] DB:", DB)
    ids = load_db_ids(DB, limit=5)
    print("[probe] first 5 dbIDs:", ids)

    with tarfile.open(TAR, "r:") as tar:
        for dbid in ids:
            name = f"QSO_S82/{dbid}"
            try:
                member = tar.getmember(name)
            except KeyError:
                print(f"[probe] MISSING in tar: {name}")
                continue
            f = tar.extractfile(member)
            lines = f.read().decode("utf-8","ignore").splitlines()
            print(f"\n[probe] dbID={dbid} lines={len(lines)} first line token check:")
            if lines:
                n_tok, preview = extract_i_triplet_tokens(lines[0])
                print("  tokens on line 1:", n_tok)
                print("  first ~18 tokens:", preview)

            mjd, mag, err, bad = extract_i_band(lines)
            print(f"  extracted i-band points: {len(mag)} (skipped/bad lines: {bad})")
            if len(mag) >= 5:
                print("  sample mjd[:3], mag[:3], err[:3]:", mjd[:3], mag[:3], err[:3])

    print("\n[probe] done.")

if __name__ == "__main__":
    main()