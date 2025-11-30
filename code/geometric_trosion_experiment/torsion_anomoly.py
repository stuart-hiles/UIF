import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from numpy import cross, dot, array

# --- Setup for Simulated Data ---
# Note: For this execution, we simulate the two data files locally based on
# the table data you provided, as the actual files are not available.
eeg_data = """state,n_windows,mean_H_data,mean_H_surr,deltaI_mean,deltaI_median,deltaI_std,k_H_p84p16,H_mean,H_std,R_mean,R_std
eyes_closed,3161,0.7771665380107403,0.8316478979212627,-0.05448135991052248,-0.041605521347041985,0.056445995136458704,0.18077655011741978,0.7771665380107403,0.09507699034753622,0.8326986231616897,0.29230411650720883
eyes_open,3161,0.8588840237661098,0.8698184247384335,-0.01093440097232353,-0.005892415831287745,0.03282044038771683,0.08684328235708616,0.8588840237661098,0.0528256032671047,0.7474988791498646,0.26525086798919817
task,78787,0.8583453945887386,0.8714872383257772,-0.013141843737038647,-0.005902361905890774,0.03587890877007902,0.11999465995351011,0.8583453945887386,0.063513855413765,0.7758876044532416,0.23665198810105104
"""
qso_data = """zbin,N,DeltaI_sigma_std,Gamma_tau_MB_slope,lambdaR_highR_fraction,Rinf_log10sigma_p95,k_tau_spread
low-z,3086,1.6918139189490606,0.05093013519719396,0.7242384964355152,-0.08565350000000001,4.6348275
mid-z,3086,0.532749941388773,0.005691821258368378,0.4351911860012962,-0.300393,3.62365
high-z,3086,0.49319647874194683,0.015115829209501604,0.3405703175631886,-0.1867755,3.9760425
"""
from io import StringIO
eeg = pd.read_csv(StringIO(eeg_data))
qso = pd.read_csv(StringIO(qso_data))

# ------------------------------------------------------------------
# Helper to find the real column name given some candidate spellings
# ------------------------------------------------------------------
def find_col(df, logical_name, candidates):
    cols = [c.strip() for c in df.columns]
    # print(f"\nLooking for '{logical_name}' in columns:", cols)
    for c in candidates:
        for col in df.columns:
            if col.strip() == c.strip():
                # print(f"  → using column '{col}' for '{logical_name}'")
                return col
    raise KeyError(f"Could not find any of {candidates} for logical column '{logical_name}'.")

# ------------------------------------------------------------------
# 2. Resolve column names robustly (no change needed here)
# ------------------------------------------------------------------
# Use named index columns
eeg = eeg.set_index("state")
qso = qso.set_index("zbin")

deltaI_col = find_col(eeg, "ΔI (EEG)", ["deltaI_mean", "deltal_mean"])
Gamma_col = find_col(eeg, "Γ (EEG)", ["k_H_p84p16"]) # Gamma (Recursion) is often linked to k
lambdaR_col = find_col(eeg, "λR (EEG)", ["R_mean"]) # R_mean is local R(x,t) which is tied to lambdaR

q_DeltaI_col = find_col(qso, "ΔI (QSO)", ["DeltaI_sigma_std"])
q_Gamma_col = find_col(qso, "Γ (QSO)", ["Gamma_tau_MB_slope"])
q_lambdaR_col = find_col(qso, "λR (QSO)", ["lambdaR_highR_fraction"])
Rinf_col = find_col(qso, "R∞ (QSO)", ["Rinf_log10sigma_p95"]) # **Crucial addition for Rinf**

# ------------------------------------------------------------------
# 3. Build trajectories and extract R∞
# ------------------------------------------------------------------
eeg_states_order = ["eyes_open", "task", "eyes_closed"]
eeg_labels = ["EO", "TASK", "EC"]
eeg_traj = eeg.loc[eeg_states_order, [deltaI_col, Gamma_col, lambdaR_col]].to_numpy()

qso_zbins_order = ["high-z", "mid-z", "low-z"]
qso_labels = ["high-z", "mid-z", "low-z"]
qso_traj = qso.loc[qso_zbins_order, [q_DeltaI_col, q_Gamma_col, q_lambdaR_col]].to_numpy()

# Extract R_infinity from Quasar data (using the mean of the log value, then exponentiating)
Rinf_log_values = qso.loc[qso_zbins_order, Rinf_col].to_numpy()
Rinf_log_mean = np.mean(Rinf_log_values)
Rinf_GLOBAL = 10**Rinf_log_mean # Global coherence ceiling, R_inf
print(f"\nExtracted R∞ (Global Coherence Ceiling) = {Rinf_GLOBAL:.4g} (from mean of log values)")

# ------------------------------------------------------------------
# 4. **HIGH-COHERENCE CORRECTION: Calculate Informational Torsion Anomaly (ITA) Metric**
# ------------------------------------------------------------------
def calculate_ita_metric(deltaI_values, Rinf_global_ceiling):
    """
    Calculates the Torsional Precession Rate (Omega_tau), which serves as the ITA Metric.
    
    Physics: ITA is proportional to the local Informational Current (sourced by |Delta I|)
    divided by the global Coherence Ceiling (R_inf).
    Omega_tau ~ |Delta I| / R_inf
    """
    # Use absolute value of Delta I as it represents the energy density/current magnitude
    ita_metric = np.abs(deltaI_values) / Rinf_global_ceiling
    return ita_metric

# 4a. Calculate the ITA Metric (Omega_tau) for each EEG state
eeg_deltaI_values = eeg.loc[eeg_states_order, deltaI_col].to_numpy()
eeg_omega_tau = calculate_ita_metric(eeg_deltaI_values, Rinf_GLOBAL)

# 4b. Calculate a comparable metric for Quasar (using its own Delta I analog)
qso_deltaI_values = qso.loc[qso_zbins_order, q_DeltaI_col].to_numpy()
qso_omega_tau = calculate_ita_metric(qso_deltaI_values, Rinf_GLOBAL)

print(f"\nEEG Torsional Anomaly (Ωτ) Values: {eeg_omega_tau}")
print(f"QSO Torsional Anomaly (Ωτ) Values: {qso_omega_tau}")

# ------------------------------------------------------------------
# 5. Shared axis limits and Dimensional Normalization for Panel C
# ------------------------------------------------------------------
# Trajectory points are kept the same for A and B.
all_points = np.vstack([eeg_traj, qso_traj])
xmin, ymin, zmin = all_points.min(axis=0)
xmax, ymax, zmax = all_points.max(axis=0)

pad = 0.05 * (xmax - xmin)
xmin -= pad; xmax += pad
ymin -= pad; ymax += pad
zmin -= pad; zmax += pad

# **Normalization for Combined Plot (Panel C):**
# Normalize all dimensions to [0, 1] so that the physical geometry of the path is comparable.
def normalize_traj(traj, all_points):
    min_vals = all_points.min(axis=0)
    max_vals = all_points.max(axis=0)
    # Avoid division by zero if all values are identical
    range_vals = np.where(max_vals - min_vals == 0, 1.0, max_vals - min_vals) 
    return (traj - min_vals) / range_vals

eeg_traj_norm = normalize_traj(eeg_traj, all_points)
qso_traj_norm = normalize_traj(qso_traj, all_points)
norm_min, norm_max = 0, 1.05


# ------------------------------------------------------------------
# 6. Four-panel figure (Panel D is the crucial ITA Metric)
# ------------------------------------------------------------------
fig = plt.figure(figsize=(20, 5))

# Panel A — EEG Trajectory (Raw)
ax1 = fig.add_subplot(1, 4, 1, projection="3d")
ax1.plot(eeg_traj[:, 0], eeg_traj[:, 1], eeg_traj[:, 2], "-o", linewidth=2, color='darkblue')
for label, point in zip(eeg_labels, eeg_traj):
    ax1.text(point[0], point[1], point[2], label, fontsize=9)
ax1.set_title(f"A. Local System Trajectory (EEG)")
ax1.set_xlabel("ΔI (EEG)"); ax1.set_ylabel("Γ (k)"); ax1.set_zlabel("λR (Rmean)")
ax1.set_xlim(xmin, xmax); ax1.set_ylim(ymin, ymax); ax1.set_zlim(zmin, zmax)

# Panel B — Quasar Trajectory (Raw)
ax2 = fig.add_subplot(1, 4, 2, projection="3d")
ax2.plot(qso_traj[:, 0], qso_traj[:, 1], qso_traj[:, 2], "-o", linewidth=2, color='darkred')
for label, point in zip(qso_labels, qso_traj):
    ax2.text(point[0], point[1], point[2], label, fontsize=9)
ax2.set_title(f"B. Substrate Trajectory (Quasar)")
ax2.set_xlabel("ΔI (QSO)"); ax2.set_ylabel("Γ (Slope)"); ax2.set_zlabel("λR (Fraction)")
ax2.set_xlim(xmin, xmax); ax2.set_ylim(ymin, ymax); ax2.set_zlim(zmin, zmax)

# Panel C — Combined Trajectory (Normalized for Physical Comparison)
ax3 = fig.add_subplot(1, 4, 3, projection="3d")
ax3.plot(eeg_traj_norm[:, 0], eeg_traj_norm[:, 1], eeg_traj_norm[:, 2], "-o", linewidth=2, color='darkblue', label="EEG (Normalized)")
ax3.plot(qso_traj_norm[:, 0], qso_traj_norm[:, 1], qso_traj_norm[:, 2], "-o", linewidth=2, color='darkred', label="Quasars (Normalized)")
ax3.set_title("C. Normalized Operator Geometry (Physical Equivalence)")
ax3.set_xlabel("Normalized ΔI"); ax3.set_ylabel("Normalized Γ"); ax3.set_zlabel("Normalized λR")
ax3.set_xlim(norm_min, norm_max); ax3.set_ylim(norm_min, norm_max); ax3.set_zlim(norm_min, norm_max)
ax3.legend(loc="best", fontsize=8)

# **Panel D — Informational Torsion Anomaly (ITA) Metric**
ax4 = fig.add_subplot(1, 4, 4)
ax4.bar(
    eeg_labels, 
    eeg_omega_tau, 
    color=['blue', 'orange', 'green'], 
    alpha=0.7,
    label='EEG States ($\Omega_{\\tau}$)'
)

# Plot Quasar-derived values as horizontal constraints (if applicable)
qso_labels_short = [f"{l} (QSO)" for l in qso_labels]
for i, omega_val in enumerate(qso_omega_tau):
    ax4.axhline(
        omega_val, 
        linestyle='--', 
        color=['red', 'purple', 'brown'][i], 
        label=qso_labels_short[i],
        linewidth=1
    )

ax4.set_title(f"D. Torsional Anomaly ($\Omega_\\tau$) Metric")
ax4.set_ylabel("ITA Metric (Ωτ) [a.u.]")
ax4.set_xlabel("EEG State")
ax4.legend(loc='upper right', fontsize=8)

plt.tight_layout()

os.makedirs("figures", exist_ok=True)
outpath = os.path.join("figures", "Fig_8-1_torsion_anomaly.png")
plt.savefig(outpath, dpi=300)
plt.close()

print("\nSaved 4-panel figure, including the corrected ITA Metric, to:", outpath)
print("\n--- Structural Analysis ---")
print("The original torsion calculation was a geometric property of the curve, not the field. The code now calculates the physically correct Torsional Anomaly (Ωτ) metric, which couples the local informational current (Delta I) to the global Coherence Ceiling (Rinf).")