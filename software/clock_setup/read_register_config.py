#!/usr/bin/env python3

import csv
from typing import List, NamedTuple


class Register(NamedTuple):
    """Defines a single register

    Attributes:
        address (str): The register address.
        value   (str): The register value.
    """

    address: int
    value: int


def read_register_config(register_config: str) -> List[Register]:
    """Read the register config from the given file

    :param register_config: The file where the register configuration is defined.
    :type register_config: str
    :return: A list containing the register configuration given as a tuple of address and value.
    """
    values = []
    with open(register_config, newline="") as config:
        config_reader = csv.reader(config)
        for row in config_reader:
            # exculde any header lines
            if not row[0].startswith("#"):
                address = int(row[0])
                value = int(row[1][:-1], 16)  # strip the 'h' from the number
                register = Register(address, value)
                values.append(register)

    return values
