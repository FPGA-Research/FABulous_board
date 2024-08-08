#!/usr/bin/env python3

import argparse
from argparse import Namespace
from pyftdi.i2c import I2cController, I2cPort
from pyftdi.ftdi import Ftdi
import modules.ftdi_access as fa
from clock_setup.read_register_config import read_register_config, Register
from typing import List

DEVICE_ADDRESS = 0x60

REGISTER_DEVICE_STATUS = 0
REGISTER_OUTPUT_ENABLE = 3
REGISTER_CLK0_CONTROL = 16
REGISTER_PLL_RESET = 177

LOS_XTAL = 1 << 0x3


def __setup_parser() -> Namespace:
    """Parse the command line arguments.

    :returns: The parsed arguments.
    """
    # Create the parser
    parser = argparse.ArgumentParser(
        description="Configures the Si5351A clock generator."
    )

    # Add arguments
    parser.add_argument(
        "register_config",
        type=str,
        help="Specifies the register config to be used.",
    )

    # Parse the arguments
    args = parser.parse_args()

    return args


def __set_clocks(i2c_port: I2cPort) -> None:
    """Set the clocks of the SI5351A-B

    :param i2c_port: The I2C port to be used.
    :type i2c_port: I2cPort
    """
    i2c_port = __config_i2c(DEVICE_ADDRESS)

    # Send one byte, then receive one byte
    # slave.exchange([0x04], 1)

    # Write a register to the I2C slave
    # slave.write_to(0x06, b"\x00")

    # Read a register from the I2C slave
    for address in range(0xFF):
        try:
            print(i2c_port.read_from(address, 1))
        except:
            print(f"Did not respond for register: {address}")


def __config_i2c(address: int) -> I2cPort:
    """Configure the I2C controller.

    :param address: The address of the device with which to communicate.
    :return: The I2C port that can be used for communication.
    """
    i2c = I2cController()

    ftdi = Ftdi()
    device = fa.read_and_check_device_urls(ftdi)
    i2c.configure(device)

    # Get a port to an I2C slave device
    return i2c.get_port(address)


def __check_clock(value, min=1, max=50) -> None:
    """Check a clock value for valid frequencies.

    :param value: The value to be checked.
    :param min: The minimum allowed clock value.
    :param max: The maximum allowed clock value.
    """
    if value < min or value > max:
        print(f"Please select a clock between 1 MHz and 50 MHz (inclusive).")
        exit(1)


def __check_crystal(i2c_port: I2cPort):
    """Check the status of the external crystal.

    :param i2c_port: The I2c port to be used.
    """
    status = i2c_port.read_from(REGISTER_DEVICE_STATUS, 1)
    if int(status) & LOS_XTAL:
        print(
            f"ERROR: Crystal loss of signal bit set. There seems to be a problem with the crystal or its configuration."
        )
        exit(1)


def __programming_procedure(i2c_port: I2cPort, registers: List[Register]):
    """This implements the programming procedure described in figure 10 of the datasheet

    :param i2c_port: The I2C port to be used.
    :type i2c_port: I2cPort
    """

    # Disable outputs
    i2c_port.write_to(REGISTER_OUTPUT_ENABLE, b"\xFF")

    # Power down all output drivers
    i2c_port.write_to(REGISTER_CLK0_CONTROL, b"\x80", relax=False)

    # TODO: check if this works
    i2c_port.write([0x80] * 7)  # Burst write up to register 23

    # Set interrupt masks
    i2c_port.write_to(registers[0].address, bytes(registers[0].value))

    # Write config (start after register 3)
    for reg in registers[2:]:
        i2c_port.write_to(reg.address, bytes(reg.value))

    # Apply PLLA and PLLB soft reset
    i2c_port.write_to(REGISTER_PLL_RESET, b"\xAC")

    # Enable outputs for CLK0, CLK1 and CLK2
    i2c_port.write_to(registers[1].address, bytes(registers[1].value))


def program_clock_ic(register_config_file: str):
    """Program the clock IC with the given clock values and the register config file.

    :param register_config_file: The config file containing the register values created by Clock Builder Pro.
    :type register_config_file: str
    """

    registers = read_register_config(register_config_file)
    for register in registers:
        print(f"Address: {register.address}, Value: {register.value}")

    i2c_port = __config_i2c(DEVICE_ADDRESS)
    __check_crystal(i2c_port)
    __programming_procedure(i2c_port, registers)


def main():
    """The main function containing the application logic."""
    args = __setup_parser()

    program_clock_ic(args.register_config)


if __name__ == "__main__":
    main()
