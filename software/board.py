#!/usr/bin/env python3

import argparse
import sys
from clock_setup.clock_setup import program_clock_ic, CrystalError
from upload_bitstream.upload_bitstream import upload_bitstream
from pyftdi.i2c import I2cController
from loguru import logger
from modules.ftdi_access import (
    DEFAULT_FTDI_ID,
    MultipleDevicesError,
    NoDeviceFoundError,
)
from modules.usb_port_power_control import (
    power_cycle_usb_port,
    OnlyLinuxSupportedError,
    ProgramNotInstalledError,
    OutDatedLinuxKernelVersionError,
)


class Commands:
    UPLOAD_COMMAND = "upload"
    CONFIG_CLOCKS_COMMAND = "config_clocks"


def setup_logger(verbosity: int):
    # Remove the default logger to avoid duplicate logs
    logger.remove()
    logger.level("INFO", color="<green>")

    # Define logger format
    if verbosity >= 1:
        log_format = (
            "[<level>{level:}</level>]: "
            "<cyan>[{time:DD-MM-YYYY HH:mm:ss]}</cyan> | "
            "<green>[{name}</green>:<green>{function}</green>:<green>{line}]</green> - "
            "<level>{message}</level>"
        )
    else:
        log_format = "[<level>{level:}</level>]: " "<level>{message}</level>"

    # Add logger to write logs to stdout
    logger.add(sys.stdout, format=log_format, level="DEBUG", colorize=True)


def setup_parser() -> argparse.Namespace:
    """Set up the parser for the command line arguments

    :returns: The parsed arguments.
    :rtype: argsparse.Namespace
    """
    clock_command = "config_clocks"
    upload_command = "upload"
    supported_commands = [clock_command, upload_command]
    parser = argparse.ArgumentParser(description="FABulous board configuration")

    # Create subparsers for clock and upload
    subparsers = parser.add_subparsers(dest="command")

    # Define the clock arguments
    clock_parser = subparsers.add_parser(
        clock_command, help="Run the clock functionality."
    )
    clock_parser.add_argument(
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
    parser.add_argument(
        "-v",
        "--verbose",
        default=False,
        action="count",
        help="Show detailed log information including function and line number",
    )

    # Define the upload arguments
    upload_parser = subparsers.add_parser(
        upload_command, help="Run the upload functionality."
    )
    upload_parser.add_argument(
        "bitstream_file",
        type=str,
        help="Specifies the bitstream file to be uploaded.",
    )
    upload_parser.add_argument(
        "-b",
        "--baudrate",
        help="Specifies the baudrate. Defaults to 57600 which is the eFPGAs baud rate at 10 MHz.",
        type=int,
        default=57600,
    )
    upload_parser.add_argument(
        "-r",
        "--reset",
        help="""Specify if the device should be reset. Defaults to False).""",
        type=bool,
        default=False,
    )
    upload_parser.add_argument(
        "-p",
        "--usb_port",
        help="""The USB port to be turned off for the device reset (required if
        the device should be reset).""",
        type=str,
    )
    upload_parser.add_argument(
        "-l",
        "--location",
        help="The location (USB hub) of the USB port to be turned off." "",
        type=str,
    )

    # Parse the arguments
    args = parser.parse_args()

    # Check the command line parameters
    if args.command not in supported_commands:
        parser.print_help()
        exit(1)

    if args.command == Commands.UPLOAD_COMMAND and args.reset:
        if not bool(args.usb_port) or not bool(args.location):
            parser.error(
                """If the device should be reset, the USB port and hub it is
                 connected to also have to be specified!

                 Check the port and the hub using uhubctl.
                 """
            )

    return args


def main():
    """The main function containing the application logic."""
    args = setup_parser()
    i2c = I2cController()
    setup_logger(args.verbose)

    try:
        match args.command:
            case Commands.CONFIG_CLOCKS_COMMAND:
                program_clock_ic(args.register_config, i2c, args.device_id)
            case Commands.UPLOAD_COMMAND:
                if args.reset:
                    power_cycle_usb_port(args.location, args.usb_port)

                upload_bitstream(args.bitstream_file, args.baudrate, args.device_id)

            case _:
                # Should already be handled by argparse
                logger.error(f"Command {args.command} is unknown")

    except KeyboardInterrupt:
        i2c.close()
        logger.info("Exiting...")
        # Just catch all known errors and exit
    except (
        OnlyLinuxSupportedError,
        OutDatedLinuxKernelVersionError,
        ProgramNotInstalledError,
        FileNotFoundError,
        CrystalError,
        MultipleDevicesError,
        NoDeviceFoundError,
    ):
        exit(1)


if __name__ == "__main__":

    main()
