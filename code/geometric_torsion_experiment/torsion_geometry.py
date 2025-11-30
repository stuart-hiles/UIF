import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy.linalg import norm
from numpy import cross

# --- 1. Load Data from CSV Files ---
# The script expects 'eeg_operator_summary.csv' and 'quasar_variability_operators.csv'
# to be in the same directory.

try:
    # EEG Data: Trajectory is Eyes Open -> Task -> Eyes Closed
    # Assumes 'state' is the index column (e.g., 'eyes_closed', 'eyes_open', 'task')
    eeg = pd.read_csv("eeg_operator_summary.csv").set_index("state")
    print("Successfully loaded 'eeg_operator_summary.csv'")
except FileNotFoundError:
    print("ERROR: 'eeg_operator_summary.csv' not found. Please ensure the file is in the script's directory.")
    exit()

try:
    # QSO Data: Trajectory is High-z -> Mid-z -> Low-z
    # Assumes 'zbin' is the index column (e.g., 'low-z', 'mid-z', 'high-z')
    qso = pd.read_csv("quasar_variability_operators.csv").set_index("zbin")
    print("Successfully loaded 'quasar_variability_operators.csv'")
except FileNotFoundError:
    print("ERROR: 'quasar_variability_operators.csv' not found. Please ensure the file is in the script's directory.")
    exit()


# Define the columns (operators) and trajectory order
eeg_cols = ["deltaI_mean", "k_H_p84p16", "R_mean"]
qso_cols = ["DeltaI_sigma_std", "Gamma_tau_MB_slope", "lambdaR_highR_fraction"]
eeg_states_order = ["eyes_open", "task", "eyes_closed"]
qso_zbins_order = ["high-z", "mid-z", "low-z"]

# --- 2. Geometric Torsion Metric Function ---
def torsion_geometry(traj):
    """
    Computes the discrete geometric torsion metric tau_d.
    tau_d = C_z / (||Delta O1|| * ||Delta O2||)
    where C = Delta O1 x Delta O2 and C_z is the projection onto the third axis (index 2).
    
    A 3-point trajectory (O1, O2, O3) in 3D operator space is required.
    """
    if traj.shape != (3, 3):
        # Should not happen with correctly loaded data
        return 0.0

    # Step vectors along the 3-point trajectory
    d1 = traj[1] - traj[0]  # O2 - O1
    d2 = traj[2] - traj[1]  # O3 - O2

    # The vector C is the cross product, which is orthogonal to the plane spanned by d1 and d2
    C = cross(d1, d2)
    
    denom = norm(d1) * norm(d2)

    if denom < 1e-12:  # Avoid division by zero for negligible movement
        return 0.0

    # The geometric torsion is the projection of the curvature vector (C) 
    # onto the Z-axis (the third operator, index 2) normalized by step distance
    tau = C[2] / denom
    return tau

# --- 3. Bootstrapping and Normalization Function ---
def bootstrap_torsion(df, col_means, states_order, n_samples=10000, normalization=True):
    """
    Samples from the means +/- std (or a proxy) to generate a distribution of tau_d.
    The distribution allows for the computation of the mean torsion and a 68% CI.
    """
    tau_samples = []

    means_df = df.loc[states_order, col_means]
    
    # Logic to infer or proxy for standard deviations
    stds_df = pd.DataFrame(index=states_order, columns=col_means)
    for col in means_df.columns:
        # 1. Try to find an explicit '_std' column
        std_col_name = col.replace("_mean", "_std")
        if std_col_name in df.columns:
            stds_df[col] = df.loc[states_order, std_col_name]
        # 2. Use a specific proxy for k_H_p84p16 using H_std (as per original data structure)
        elif col == "k_H_p84p16" and "H_std" in df.columns:
            stds_df[col] = df.loc[states_order, "H_std"]
        # 3. Default proxy: 10% relative error (used primarily for QSO data which lacks explicit std columns)
        else:
            stds_df[col] = np.abs(means_df[col]) * 0.1
    
    means = means_df.to_numpy()
    stds = stds_df.to_numpy()
    
    # Compute global normalization parameters from the mean data for stability
    global_means = means.flatten().mean()
    global_stds = means.flatten().std()

    for _ in range(n_samples):
        # 1. Generate a sampled trajectory by drawing from a normal distribution
        traj_sample = np.random.normal(loc=means, scale=stds)
        
        # 2. Normalize the sampled trajectory (Z-score normalization)
        if normalization and global_stds > 1e-12:
            traj_norm = (traj_sample - global_means) / global_stds
        else:
            traj_norm = traj_sample
        
        # 3. Compute torsion
        tau_samples.append(torsion_geometry(traj_norm))

    tau_samples = np.array(tau_samples)
    
    mean_tau = np.mean(tau_samples)
    # Calculate 68% Confidence Interval (1 sigma equivalent)
    ci_lower = np.percentile(tau_samples, 16)
    ci_upper = np.percentile(tau_samples, 84)
    ci_error = (ci_upper - ci_lower) / 2
    
    return mean_tau, ci_error

# --- 4. Execute Analysis ---
N_SAMPLES = 10000 # Number of bootstrap samples

# EEG Torsion Calculation
eeg_tau, eeg_ci = bootstrap_torsion(
    df=eeg, 
    col_means=eeg_cols, 
    states_order=eeg_states_order, 
    n_samples=N_SAMPLES,
    normalization=True
)

# QSO Torsion Calculation
qso_tau, qso_ci = bootstrap_torsion(
    df=qso, 
    col_means=qso_cols, 
    states_order=qso_zbins_order, 
    n_samples=N_SAMPLES,
    normalization=True
)

# Print Summary Results
print("\n--- Results (Geometric Torsion τd) ---")
print(f"EEG Torsion (τ_EEG): {eeg_tau:+.4f} ± {eeg_ci:.4f} (68% CI, N={N_SAMPLES})")
print(f"QSO Torsion (τ_QSO): {qso_tau:+.4f} ± {qso_ci:.4f} (68% CI, N={N_SAMPLES})")
print("---------------------------------------")

# --- 5. Visualization (Bar Plot) ---
labels = [r"$\tau_{\text{EEG}}$ (Local System)", r"$\tau_{\text{QSO}}$ (Cosmic Substrate)"]
means = [eeg_tau, qso_tau]
errors = [eeg_ci, qso_ci]

# Create the figure and axes
fig, ax = plt.subplots(figsize=(7, 6))

bars = ax.bar(
    labels, 
    means, 
    yerr=errors, 
    capsize=5, 
    color=['darkblue', 'darkred'],
    alpha=0.7
)

# Add value labels
for bar, mean, error in zip(bars, means, errors):
    y_pos = mean + error * 1.5 if mean >= 0 else mean - error * 2.5
    ax.text(
        bar.get_x() + bar.get_width() / 2, 
        y_pos, 
        f'{mean:+.3f}', 
        ha='center', 
        va='center',
        fontsize=10,
        fontweight='bold'
    )

ax.axhline(0, color='black', linestyle='--', linewidth=0.8) # Zero line

ax.set_title(r"Geometric Torsion ($\tau_d$) of Operator Trajectories", fontsize=14)
ax.set_ylabel(r"Informational Torsion Metric ($\tau_d$) [Dimensionless]", fontsize=12)

# Adjust y-limits dynamically
ymin_data = min(means[i] - errors[i] for i in range(len(means)))
ymax_data = max(means[i] + errors[i] for i in range(len(means)))
padding = (ymax_data - ymin_data) * 0.15
ax.set_ylim(ymin_data - padding, ymax_data + padding)
ax.tick_params(axis='x', rotation=0)

plt.tight_layout()

# Save the figure
outpath = "Fig_Geometric_Torsion_Comparison.png"
plt.savefig(outpath, dpi=300)
print(f"Figure saved to '{outpath}'")
# plt.show() # Uncomment to display the figure immediately