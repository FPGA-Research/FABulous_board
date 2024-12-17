#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import argparse
from pathlib import Path
from termcolor import colored
from typing import Tuple

width = 120
height = 100


def parse_arguments() -> argparse.Namespace:
    """Parse the command line arguments.

    :return: The arguments parsed from the command line.
    :rtype: argparse.Namespace
    """

    parser = argparse.ArgumentParser(prog="plot.py")
    parser.add_argument("circuit_name", help="The name of the circuit.")
    parser.add_argument(
        "-s", "--show", help="Directly show the plot.", action="store_true"
    )
    args = parser.parse_args()
    return args


def plot(
    circuit_name: str,
    data: np.ndarray[Tuple[int, int], np.dtype[np.float64]],
    x_label: str,
    y_label: str,
    show: bool,
) -> None:
    """Plot the data

    :param xlabel: The label of the x-axis.
    :type circuit_name: str
    :param ylabel: The label of the y-axis.
    :type suffix: str
    """
    plt.figure(figsize=(width / 25.4, height / 25.4))
    plt.plot(data[:, 0], data[:, 1])
    plt.grid()
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.tight_layout()
    pdf_file = _get_relative_file_path(circuit_name, ".pdf")
    pgf_file = _get_relative_file_path(circuit_name, ".pgf")
    plt.savefig(pdf_file)
    plt.savefig(pgf_file)
    if show:
        plt.show()
    else:
        print(f'Plot for circuit "{circuit_name}" generated!')


def _get_relative_file_path(circuit_name: str, suffix: str) -> str:
    """Get the relative path to the file

    :param circuit_name: The name of the circuit.
    :type circuit_name: str
    :param suffix: The suffix of the file.
    :type suffix: str
    :return: The relative file path.
    :rtype: str
    """
    file_path = "./" + circuit_name + "/" + circuit_name + suffix
    _check_if_file_exists(file_path)
    return file_path


def _check_if_file_exists(file_path: str) -> None:
    """Check if a file exists.
    Write an error message and exit if it does not exist.
    """
    file = Path(file_path)
    if not file.is_file():
        print(
            colored("Error: ", "red")
            + f"""File "{file_path}" does not exist.
       Check for spelling and if the data was exported for the circuit."""
        )
        exit(1)


def main() -> None:
    args = parse_arguments()
    circuit_name = args.circuit_name
    data_file = _get_relative_file_path(args.circuit_name, ".txt")
    data = np.loadtxt(data_file, skiprows=1)
    plot(circuit_name, data, "$V_{in}$ [V]", "$V_{out}$ [V]", args.show)


if __name__ == "__main__":
    main()
