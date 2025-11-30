import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO
import sys

# --- 1. Data Proxies (Used for internal testing/fallback if CSVs are missing) ---
# NOTE: The script is designed to read the CSV files directly, but these blocks 
# ensure the code structure is sound and allow for easy reproduction of the core logic.

# EEG Data: Relevant columns for delta I (Informational Difference)
eeg_data_proxy = """state,deltaI_mean,deltaI_std,R_mean
eyes_closed,-0.0545,0.0564,0.8327
eyes_open,-0.0109,0.0328,0.7475
task,-0.0131,0.0359,0.7759
"""
# QSO Data: Relevant column for R_inf (Coherence Ceiling)
qso_data_proxy = """zbin,Rinf_log10sigma_p95
low-z,-0.0857
mid-z,-0.3004
high-z,-0.1868
"""

# --- 2. Load Data from CSV Files ---
def load_data_or_use_proxy():
    """Loads data from CSV files or uses proxies if not found."""
    try:
        eeg_df = pd.read_csv("eeg_operator_summary.csv").set_index("state")
        print("Successfully loaded 'eeg_operator_summary.csv'")
    except FileNotFoundError:
        print("WARNING: 'eeg_operator_summary.csv' not found. Using internal data proxy.")
        eeg_df = pd.read_csv(StringIO(eeg_data_proxy)).set_index("state")

    try:
        qso_df = pd.read_csv("quasar_variability_operators.csv").set_index("zbin")
        print("Successfully loaded 'quasar_variability_operators.csv'")
    except FileNotFoundError:
        print("WARNING: 'quasar_variability_operators.csv' not found. Using internal data proxy.")
        qso_df = pd.read_csv(StringIO(qso_data_proxy)).set_index("zbin")
        
    return eeg_df, qso_df

eeg, qso = load_data_or_use_proxy()

# Define the states and relevant columns
eeg_states_order = ["eyes_open", "task", "eyes_closed"]
deltaI_col = "deltaI_mean"
deltaI_std_col = "deltaI_std"
Rinf_qso_col = "Rinf_log10sigma_p95"


# --- 3. ITA Metric Function (Bootstrapping) ---
def bootstrap_ita_metric(eeg_df, qso_df, states_order, n_samples=10000):
    """
    Computes the Informational Torsion-Agency (ITA) Metric Omega_tau for each EEG state.
    Omega_tau(state) = Delta I(state) / R_inf(QSO)
    """
    results = {}

    # --- Step A: Setup QSO Normalizer (R_inf,QSO) ---
    # We use the R_inf proxy (log10 sigma) and assume a 10% relative error 
    # for bootstrapping its distribution, as explicit std is often unavailable.
    Rinf_means_qso = qso_df[Rinf_qso_col].to_numpy()
    Rinf_stds_qso = np.abs(Rinf_means_qso) * 0.1

    # --- Step B: Iterate and Bootstrap for each EEG state ---
    for state in states_order:
        tau_samples = []
        
        # Get mean and std for Delta I for the current EEG state
        deltaI_mean_eeg = eeg_df.loc[state, deltaI_col]
        deltaI_std_eeg = eeg_df.loc[state, deltaI_std_col]
        
        for _ in range(n_samples):
            # 1. Sample Delta I for the current EEG state
            deltaI_sample = np.random.normal(loc=deltaI_mean_eeg, scale=deltaI_std_eeg)
            
            # 2. Sample R_inf for all QSO states and calculate the mean normalizer
            Rinf_samples_qso = np.random.normal(loc=Rinf_means_qso, scale=Rinf_stds_qso)
            Rinf_qso_normalizer = np.mean(Rinf_samples_qso)
            
            # 3. Calculate the ITA Metric (Omega_tau)
            if np.abs(Rinf_qso_normalizer) > 1e-12:
                omega_tau_sample = deltaI_sample / Rinf_qso_normalizer
                tau_samples.append(omega_tau_sample)
            else:
                # Append 0 or skip if R_inf is negligible, though highly unlikely
                tau_samples.append(0.0) 

        tau_samples = np.array(tau_samples)
        
        # Compute mean and 68% Confidence Interval (16th to 84th percentile)
        mean_omega = np.mean(tau_samples)
        ci_lower = np.percentile(tau_samples, 16)
        ci_upper = np.percentile(tau_samples, 84)
        ci_error = (ci_upper - ci_lower) / 2
        
        results[state] = (mean_omega, ci_error)

    return results

# --- 4. Execute Analysis ---
N_SAMPLES = 10000 

ita_results = bootstrap_ita_metric(
    eeg_df=eeg, 
    qso_df=qso, 
    states_order=eeg_states_order, 
    n_samples=N_SAMPLES
)

# Print Summary Results
print("\n--- Results (Informational Torsion-Agency Metric, Ωτ) ---")
# Calculate the mean cosmic normalizer R_inf(QSO) for display clarity
Rinf_qso_mean = qso[Rinf_qso_col].mean()
print(f"Cosmic Normalizer R∞,QSO (Mean Rinf_log10sigma_p95): {Rinf_qso_mean:+.4f}")
print("---------------------------------------------------------")
for state, (mean_omega, ci_error) in ita_results.items():
    print(f"Ωτ({state.upper()}): {mean_omega:+.4f} ± {ci_error:.4f} (68% CI)")
print("---------------------------------------------------------")

# --- 5. Visualization (Bar Plot) ---
labels = [f"Ωτ({s.replace('_', ' ').title()})" for s in eeg_states_order]
means = [ita_results[s][0] for s in eeg_states_order]
errors = [ita_results[s][1] for s in eeg_states_order]

fig, ax = plt.subplots(figsize=(8, 6))

bars = ax.bar(
    labels, 
    means, 
    yerr=errors, 
    capsize=6, 
    color=['#4C72B0', '#55A868', '#C44E52'], # Distinct colors for states
    alpha=0.8
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
        fontsize=11,
        fontweight='bold'
    )

ax.axhline(0, color='black', linestyle='--', linewidth=0.8) # Zero line

ax.set_title(r"Informational Torsion-Agency Metric ($\Omega_{\tau}$)", fontsize=14)
ax.set_ylabel(r"ITA Metric ($\Delta I_{\text{EEG}} / R_{\infty, \text{QSO}}$) [Dimensionless]", fontsize=12)

# Adjust y-limits dynamically
ymin_data = min(means[i] - errors[i] for i in range(len(means)))
ymax_data = max(means[i] + errors[i] for i in range(len(means)))
padding = (ymax_data - ymin_data) * 0.15
ax.set_ylim(ymin_data - padding, ymax_data + padding)

plt.tight_layout()

# Save the figure
outpath = "Fig_ITA_Metric_Comparison.png"
plt.savefig(outpath, dpi=300)
print(f"\nFigure saved to '{outpath}'")
# plt.show() # Uncomment to display the figure immediately