import os, json, glob

BASE = "ut26_cosmo3d_outputs"

folders = sorted(glob.glob(os.path.join(BASE, "*")))
if not folders:
    print("No run folders found under", BASE)
    exit()

print(f"Found {len(folders)} run folders:\n")

for f in folders:
    summary_path = os.path.join(f, "summary.json")
    if not os.path.exists(summary_path):
        continue
    with open(summary_path) as fh:
        s = json.load(fh)
    tag = os.path.basename(f)
    print(f"Run: {tag}")
    print(f"  BETA={s.get('BETA')}, LAMBDA_R={s.get('LAMBDA_R')}, "
          f"ETA_THRESH={s.get('ETA_THRESH')}, DRIVE_A={s.get('DRIVE_A')}, "
          f"DRIVE_W={s.get('DRIVE_W')}, NOISE_STD={s.get('NOISE_STD')}")
    print(f"  final_mean_s={s.get('final_mean_s'):.3f}, "
          f"total_prunes={s.get('total_prunes')}\n")