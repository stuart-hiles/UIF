# run_threshold_map.py
import os, json, numpy as np
from subprocess import run

etas = [0.40, 0.50, 0.55, 0.60, 0.70]  # ETA_THRESH
lrs  = [0.10, 0.15, 0.20, 0.25, 0.30]  # LAMBDA_R

rows = []
for eta in etas:
    for lr in lrs:
        tag = f"eta{eta}_lr{lr}"
        env = os.environ.copy()
        env["ETA_THRESH"] = str(eta)
        env["LAMBDA_R"]   = str(lr)
        env["RUN_TAG"]    = tag
        print(">> Running", tag)
        run(["python", "ut26_cosmo3d.py"], env=env, check=True)

        with open(os.path.join("ut26_cosmo3d_outputs", tag, "summary.json")) as f:
            s = json.load(f)

        ms = float(s["final_mean_s"])
        pr = float(s["total_prunes"])
        # Simple regime classifier (adjust thresholds if needed)
        if pr < 1e5:
            regime = 0  # fragile/dead
        elif ms > 0.58 or ms < 0.42:
            regime = 2  # runaway/drift
        else:
            regime = 1  # stable ceiling

        rows.append([eta, lr, ms, pr, regime])

np.savetxt(os.path.join("ut26_cosmo3d_outputs", "threshold_map.csv"),
           np.array(rows, dtype=float), delimiter=",",
           header="eta,lambdaR,final_mean_s,total_prunes,regime", comments="")
print("Wrote: ut26_cosmo3d_outputs/threshold_map.csv")