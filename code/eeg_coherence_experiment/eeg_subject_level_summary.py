# UT26 EEG Subject-Level Summary (paired EC–EO + bootstrap CI + permutation p)
import os, json
import numpy as np
import pandas as pd

IN   = "outputs/EEG_windows_HCR.csv"
OUT1 = "outputs/EEG_recording_summary_R.csv"
OUT2 = "outputs/EEG_subject_summary_R.csv"
OUT3 = "outputs/EEG_effects_EC_vs_EO.json"

def main():
    if not os.path.exists(IN):
        print("Missing:", IN); return

    df = pd.read_csv(IN)

    # subject/run from rec (e.g., S001R01)
    df["subject"] = df["rec"].str.slice(0,4)
    df["run"]     = df["rec"].str.slice(4,7)

    # Recording-level means
    rec_summary = df.groupby(["subject","run","state","rec"], as_index=False)["R"].mean()
    rec_summary.to_csv(OUT1, index=False)
    print("wrote:", OUT1)

    # Subject-level means
    sub_summary = rec_summary.groupby(["subject","state"], as_index=False)["R"].mean()
    have_both = sub_summary.groupby("subject")["state"].nunique()
    keep = have_both[have_both>=2].index
    sub2 = sub_summary[sub_summary["subject"].isin(keep)].pivot(index="subject", columns="state", values="R")

    for col in ["eyes_closed","eyes_open"]:
        if col not in sub2.columns:
            sub2[col] = np.nan
    sub2 = sub2.loc[:, ["eyes_closed","eyes_open"]].dropna()

    sub2["diff"] = sub2["eyes_closed"] - sub2["eyes_open"]
    sub2.reset_index().to_csv(OUT2, index=False)
    print("wrote:", OUT2)

    diffs = sub2["diff"].values
    n = len(diffs)
    if n == 0:
        print("No paired subjects with both EC and EO."); return

    # Bootstrap CI
    rng = np.random.default_rng(42)
    B = 10000
    boot_means = [np.mean(diffs[rng.integers(0, n, n)]) for _ in range(B)]
    ci = np.quantile(boot_means, [0.025, 0.5, 0.975]).tolist()
    d_paired = float(np.mean(diffs) / (np.std(diffs, ddof=1) + 1e-12))

    # Permutation test (paired, two-sided)
    rng = np.random.default_rng(123)
    Bperm = 10000
    obs = float(np.mean(diffs))
    perm_means = []
    for _ in range(Bperm):
        signs = rng.integers(0, 2, size=n)*2 - 1
        perm_means.append(np.mean(diffs * signs))
    perm_means = np.array(perm_means)
    p_two_sided = 2.0 * min(
        (np.sum(perm_means >= obs)+1)/(Bperm+1),
        (np.sum(perm_means <= obs)+1)/(Bperm+1)
    )

    res = {
        "n_subjects": int(n),
        "mean_diff_EC_minus_EO": obs,
        "CI95_bootstrap": ci,
        "cohen_d_paired": d_paired,
        "p_perm_two_sided": float(p_two_sided)
    }
    with open(OUT3, "w") as f:
        json.dump(res, f, indent=2)
    print("wrote:", OUT3)
    print(res)

if __name__ == "__main__":
    main()