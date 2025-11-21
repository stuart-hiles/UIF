# run_gamma_sweep.py
import os, json, numpy as np
from subprocess import run

# Small, quick grid (expand if you want finer detail)
amps    = [0.4, 0.6, 0.8, 1.0]        # DRIVE_A
periods = [64, 32, 24, 16, 12, 8]     # steps per cycle
Ws      = [2*np.pi/p for p in periods]  # DRIVE_W (rad/step)

rows = []
for A in amps:
    for W, P in zip(Ws, periods):
        tag = f"A{A}_P{P}"
        env = os.environ.copy()
        env["DRIVE_A"] = str(A)
        env["DRIVE_W"] = str(W)
        env["RUN_TAG"] = tag
        print(">> Running", tag)
        run(["python", "ut26_cosmo3d.py"], env=env, check=True)

        with open(os.path.join("ut26_cosmo3d_outputs", tag, "summary.json")) as f:
            s = json.load(f)

        # simple collapse flag (tune if needed)
        collapsed = float(s["final_mean_s"]) > 0.52
        rows.append([A, W, P, s["final_mean_s"], s["total_prunes"], int(collapsed)])

np.savetxt(os.path.join("ut26_cosmo3d_outputs", "gamma_sweep.csv"),
           np.array(rows, dtype=float), delimiter=",",
           header="A,W,P,final_mean_s,total_prunes,collapsed", comments="")
print("Wrote: ut26_cosmo3d_outputs/gamma_sweep.csv")