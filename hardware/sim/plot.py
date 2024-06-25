#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt

width = 120
height = 100


circuit_name = "linear_regulator"
data_file = circuit_name + "/" + circuit_name + ".txt"
pdf_file = circuit_name + "/" + circuit_name + ".pdf"
pgf_file = circuit_name + "/" + circuit_name + ".pgf"  # used as LaTeX input


def main():
    foo = np.loadtxt(data_file)
    plt.figure(figsize=(width / 25.4, height / 25.4))
    plt.plot(foo[:, 0], foo[:, 1])
    plt.grid()
    plt.xlabel("$V_{in}$ [V]")
    plt.ylabel("$V_{out}$ [V]")
    plt.tight_layout()
    plt.savefig(pdf_file)
    plt.savefig(pgf_file)


if __name__ == "__main__":
    main()
