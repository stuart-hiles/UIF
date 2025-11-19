import os
import pandas as pd

# ---------------------------------------------------------------------
# Paths – all RELATIVE to the current working directory
# ---------------------------------------------------------------------

# Folder containing the raw data files (where this script is)
BASE_DIR = os.getcwd()

MASTER_PATH = os.path.join(BASE_DIR, "master_QSO_S82.dat")
DRW_I_PATH = os.path.join(BASE_DIR, "s82drw_i.dat")

# Create output folder (relative)
OUT_DIR = os.path.join(BASE_DIR, "output", "quasar_variability_experiment")
os.makedirs(OUT_DIR, exist_ok=True)

print(f"Using base directory: {BASE_DIR}")
print(f"MASTER_PATH = {MASTER_PATH}")
print(f"DRW_I_PATH  = {DRW_I_PATH}")
print(f"Output dir  = {OUT_DIR}")

# ---------------------------------------------------------------------
# 1. Read master_QSO_S82.dat (fixed-width file)
# ---------------------------------------------------------------------
master_colspecs = [
    (0, 18),    # SDSS ID
    (19, 29),   # RAdeg
    (30, 40),   # DEdeg
    (41, 47),   # z
    (88, 94),   # apparent i magnitude
    (94, 100),  # i mag error
    (223, 230), # absolute i magnitude (Mi)
    (231, 237), # D(g-i)
]

master_names = [
    "SDSS_ID",
    "RA_deg",
    "Dec_deg",
    "z",
    "i_mag_app",
    "i_mag_err",
    "iMag_abs",
    "D_g_minus_i",
]

print("Reading MASTER catalog...")
master = pd.read_fwf(
    MASTER_PATH,
    colspecs=master_colspecs,
    names=master_names,
    comment="#",
)

master["SDSS_ID"] = master["SDSS_ID"].str.strip()

for c in ["RA_deg", "Dec_deg", "z", "i_mag_app", "i_mag_err", "iMag_abs", "D_g_minus_i"]:
    master[c] = pd.to_numeric(master[c], errors="coerce")

master["RA6"] = master["RA_deg"].round(6)
master["Dec6"] = master["Dec_deg"].round(6)

print(f"MASTER rows read: {len(master)}")

# ---------------------------------------------------------------------
# 2. Read DRW i-band file
# ---------------------------------------------------------------------
drw_cols = [
    "SDR5ID", "ra", "dec", "redshift", "M_i", "mass_BH", "chi2_pdf",
    "log10_tau", "log10_sigma", "log10_tau_lo", "log10_tau_hi",
    "log10_sig_lo", "log10_sig_hi", "edge_flag",
    "Plike", "Pnoise", "Pinf", "mu", "npts",
]

print("Reading DRW i-band variability file...")
drw_i = pd.read_csv(
    DRW_I_PATH,
    comment="#",
    delim_whitespace=True,
    names=drw_cols,
)

for c in drw_cols:
    drw_i[c] = pd.to_numeric(drw_i[c], errors="coerce")

drw_i["RA6"] = drw_i["ra"].round(6)
drw_i["Dec6"] = drw_i["dec"].round(6)

print(f"DRW rows read: {len(drw_i)}")

# ---------------------------------------------------------------------
# 3. Merge DRW parameters with master catalog
# ---------------------------------------------------------------------
print("Merging MASTER + DRW tables...")

merged = pd.merge(
    drw_i,
    master,
    on=["RA6", "Dec6"],
    how="left",
    validate="m:1",
)

n_unmatched = merged["SDSS_ID"].isna().sum()
if n_unmatched > 0:
    print(f"WARNING: {n_unmatched} rows did NOT match the master catalog.")
else:
    print("All rows successfully matched to the master catalog.")

# ---------------------------------------------------------------------
# 4. Select & rename columns for UIF output
# ---------------------------------------------------------------------
rename_map = {
    "SDSS_ID": "sdss_id",
    "ra": "ra_deg",
    "dec": "dec_deg",
    "redshift": "z",
    "M_i": "M_i",
    "mass_BH": "log10_M_BH",
    "chi2_pdf": "chi2_pdf",
    "log10_tau": "log10_tau_days",
    "log10_sigma": "log10_sigma_mag_per_sqrtyr",
    "log10_tau_lo": "log10_tau_lo",
    "log10_tau_hi": "log10_tau_hi",
    "log10_sig_lo": "log10_sigma_lo",
    "log10_sig_hi": "log10_sigma_hi",
    "edge_flag": "edge_flag",
    "Plike": "P_like",
    "Pnoise": "P_noise",
    "Pinf": "P_inf",
    "mu": "mu",
    "npts": "n_points",
    "iMag_abs": "M_i_abs",
    "D_g_minus_i": "D_g_minus_i",
}

out_df = merged.rename(columns=rename_map)
out_df = out_df[list(rename_map.values())]

print("\nPreview of merged table:")
print(out_df.head())

# ---------------------------------------------------------------------
# 5. Write output CSV
# ---------------------------------------------------------------------
out_path = os.path.join(OUT_DIR, "quasar_variability_i.csv")
out_df.to_csv(out_path, index=False)

print(f"\nWROTE OUTPUT FILE:\n  {out_path}")