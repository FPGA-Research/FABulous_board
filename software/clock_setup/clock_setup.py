#!/usr/bin/env python3

import argparse
from argparse import Namespace
from pyftdi.i2c import I2cController, I2cPort, I2cNackError
from clock_setup.read_register_config import read_register_config, Register
from typing import List
from loguru import logger
from modules.ftdi_access import DEFAULT_FTDI_ID, get_device_url

DEVICE_I2C_ADDRESS = 0x60

REGISTER_DEVICE_STATUS = 0
REGISTER_OUTPUT_ENABLE = 3
REGISTER_CLK0_CONTROL = 16
REGISTER_PLL_RESET = 177
REGISTER_CRYSTAL_INTERNAL_LOAD_CAPACITANCE = 183

LOS_XTAL = 1 << 0x3
XTAL_CL = 3 << 0x6


class I2cConnectionError(Exception):
    """An exception to be thrown when the I2C connection failed."""


class CrystalError(Exception):
    """An exception to be thrown when the crystal loss of signal bit is set."""


def __setup_parser() -> Namespace:
    """Parse the command line arguments.

    :returns: The parsed arguments.
    :rtype: Namespace
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
    parser.add_argument(
        "-i",
        "--device_id",
        help=f"""Specify the ID of the FDTI board. Find it out using lsusb.
        Defaults to {DEFAULT_FTDI_ID}""",
        type=str,
        default=DEFAULT_FTDI_ID,
    )

    # Parse the arguments
    args = parser.parse_args()

    return args


def __config_i2c(i2c: I2cController, address: int, device_id: str) -> I2cPort | None:
    """Configure the I2C controller.

    :param i2c: The I2C controller to be used.
    :type i2c: I2cController
    :param address: The address of the device with which to communicate.
    :type address: int
    :param device_id: The device ID of the device to be used for the I2C
    communication.
    :type device_id: str
    :returns: The I2C port that can be used for communication.
    :rtype: I2cPort | None
    """

    i2c_port = None
    connection_successful = False
    while not connection_successful:
        device_url = get_device_url(device_id)
        if device_url is not None:
            i2c.configure(device_url)
        # Get a port to an I2C device
        i2c_port = i2c.get_port(address)
        try:
            __check_connection(i2c_port)
            connection_successful = True
        except (I2cNackError, I2cConnectionError):
            logger.error(
                "I2C connection failed. Please check the connection or"
                + " select another device!"
            )
            i2c.flush()
            i2c.close()

    return i2c_port


def __check_connection(i2c_port: I2cPort) -> None:
    """
    Check the connection by reading the load capacitance register.


    :param i2c_port: The I2c port to be used.
    :type i2c_port: I2cPort
    """
    value = i2c_port.read_from(REGISTER_CRYSTAL_INTERNAL_LOAD_CAPACITANCE, 1)

    if (int.from_bytes(value, byteorder="big") & XTAL_CL) == 0:
        raise I2cConnectionError


def __check_crystal(i2c_port: I2cPort) -> None:
    """Check the status of the external crystal.

    :param i2c_port: The I2c port to be used.
    :type i2c_port: I2cPort
    """

    logger.info("Checking crystal...")
    status = i2c_port.read_from(REGISTER_DEVICE_STATUS, 1)

    if int.from_bytes(status, byteorder="big") & LOS_XTAL:
        logger.error(
            "Crystal loss of signal bit set. There seems to be a problem"
            + "with the crystal or its configuration."
        )
        raise CrystalError
    logger.info("Crystal OK!")


def __programming_procedure(i2c_port: I2cPort, registers: List[Register]) -> None:
    """This implements the programming procedure described in figure 10 of the datasheet

    :param i2c_port: The I2C port to be used.
    :type i2c_port: I2cPort
    """

    logger.info("Start writing the configuration...")
    # Disable outputs
    i2c_port.write_to(REGISTER_OUTPUT_ENABLE, b"\xFF")

    # Power down all output drivers

    i2c_port.write(
        [REGISTER_CLK0_CONTROL] + [0x80] * 7
    )  # Burst write up to register 23

    # Set interrupt masks
    i2c_port.write_to(registers[0].address, [registers[0].value])

    # Write config (start after register 3)
    for reg in registers[2:]:
        i2c_port.write_to(reg.address, [reg.value])

    # Apply PLLA and PLLB soft reset
    i2c_port.write_to(REGISTER_PLL_RESET, b"\xAC")

    # Enable outputs for CLK0, CLK1 and CLK2
    i2c_port.write_to(registers[1].address, [registers[1].value])
    logger.info("Configuration written!")


def program_clock_ic(
    register_config_file: str, i2c: I2cController, device_id: str
) -> None:
    """Program the clock IC with the register config file.

    :param register_config_file: The config file containing the register values created by Clock Builder Pro.
    :type register_config_file: str
    :param i2c: The I2cController instance to be used.
    :type i2c: I2cController
    :param device_id: The device ID of the device to be used for the I2C
    communication.
    :type device_id: str
    """

    registers = read_register_config(register_config_file)

    i2c = I2cController()
    i2c_port = __config_i2c(i2c, DEVICE_I2C_ADDRESS, device_id)
    if i2c_port is not None:
        __check_crystal(i2c_port)
        __programming_procedure(i2c_port, registers)
    i2c.close()


def main() -> None:
    """The main function containing the application logic."""
    args = __setup_parser()

    program_clock_ic(args.register_config, I2cController(), "0403:6014")


if __name__ == "__main__":
    main()
