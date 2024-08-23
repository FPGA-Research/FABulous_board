#!/usr/bin/env python3

from clock_setup.clock_setup import program_clock_ic
from upload_bitstream.upload_bitstream import upload_bitstream
import argparse


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

    # Parse the arguments
    args = parser.parse_args()

    # Check the command line parameters
    if args.command not in supported_commands:
        parser.print_help()
        exit(0)

    return args


def main():
    """The main function containing the application logic."""
    args = setup_parser()

    match args.command:
        case "config_clocks":
            program_clock_ic(args.register_config)
        case "upload":
            upload_bitstream(args.bitstream_file, args.baudrate)

        case _:
            print("Test")


if __name__ == "__main__":

    main()
