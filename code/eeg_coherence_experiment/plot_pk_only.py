"""
UT26 cosmology-lite: plot P(k) from pk.csv
"""

import os
import numpy as np
import matplotlib.pyplot as plt

OUTDIR = "ut26_cosmo3d_outputs"

def plot_pk(pk_csv, out_png):
    if not os.path.exists(pk_csv):
        print("Missing:", pk_csv)
        return

    data = np.genfromtxt(pk_csv, delimiter=",", names=True)
    k = data['k']
    Pk = data[list(data.dtype.names)[1]]  # second column, usually 'Pk'

    plt.figure(figsize=(6,5))
    plt.semilogy(k, np.maximum(Pk, 1e-12), lw=1.8, color="navy")
    plt.xlabel("k")
    plt.ylabel("P(k) (log scale)")
    plt.title("Toy matter power spectrum with BAO preserved")
    plt.grid(alpha=0.3, which='both')
    plt.tight_layout()
    plt.savefig(out_png, dpi=150)
    plt.close()
    print("wrote:", out_png)

def main():
    pk_csv  = os.path.join(OUTDIR, "pk.csv")
    pk_png  = os.path.join(OUTDIR, "Fig_pk.png")
    plot_pk(pk_csv, pk_png)

if __name__ == "__main__":
    main()