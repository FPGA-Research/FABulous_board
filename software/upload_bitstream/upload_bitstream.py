#!/usr/bin/env python3

import serial
import serial.tools.list_ports
import argparse
from pathlib import Path
from loguru import logger
from modules.ftdi_access import DEFAULT_FTDI_ID, get_device_path_for_device_id

DEFAULT_BAUDRATE = 57600


def read_bitstream_data(bitstream_file: str) -> bytearray:
    """Read the bitstream data from the specified file.

    :param bitstream_file: The bitstream file to be read.
    :type bitstream_file: str
    :return: The bitstream data read from the file.
    :rtype: bytearray
    """
    file = Path(bitstream_file)
    if not file.is_file():
        logger.error(
            f"File {bitstream_file} does not exist."
            + " Check for spelling and if a bitstream file was created."
        )
        raise FileNotFoundError

    with open(bitstream_file, "rb") as f:
        data = bytearray(f.read())

    return data


def upload_bitstream(bitstream_file: str, baudrate: int, ftdi_name: str) -> None:
    """Upload the bitstream to the eFPGA.

    :param bitstream_file: The bitstream file to be uploaded.
    :type bitstream_file: str
    :param baudrate: The baudrate to be used for the upload.
    :type bitstream_file: str
    :param ftdi_name: The name of the FTDI chip to be used.
    :type bitstream_file: str
    """
    logger.info("Checking device...")

    device_path = get_device_path_for_device_id(ftdi_name)

    logger.info(f"Using device at {device_path}")

    data = read_bitstream_data(bitstream_file)

    
    # Needed to bring the UART module into desync state
    desync_word = [0x00, 0x10, 0, 0]
    logger.info("Uploading bitstream...")

    with serial.Serial(device_path, baudrate) as ser:
        ser.write(data)
        ser.write(bytearray(desync_word))

    logger.info("Bitstream transmitted!")


def __parse_arguments() -> argparse.Namespace:
    """Parse the command line arguments.

    :return: The arguments parsed from the command line.
    :rtype: argparse.Namespace
    """

    parser = argparse.ArgumentParser(prog="upload_bitstream.py")
    parser.add_argument(
        "bitstream_file", help="Specifies the bitstream file to be uploaded."
    )
    parser.add_argument(
        "-b",
        "--baudrate",
        help=f"Specifies the baudrate. Defaults to {DEFAULT_BAUDRATE} which is the eFPGAs"
        + " baud rate at 10 MHz in MPW-2.",
        type=int,
        default=DEFAULT_BAUDRATE,
    )
    parser.add_argument(
        "-i",
        "--device_id",
        help=f"Specifies the ID of the FTDI board. Defaults to {DEFAULT_FTDI_ID}.",
        type=str,
        default=DEFAULT_FTDI_ID,
    )
    args = parser.parse_args()
    return args


def main() -> None:
    """The main function containing the application logic"""
    args = __parse_arguments()
    upload_bitstream(args.bitstream_file, args.baudrate, args.device_id)


if __name__ == "__main__":
    main()
