#!/usr/bin/env python3

import serial
import serial.tools.list_ports
import argparse
from termcolor import colored
from pathlib import Path
from typing import List


def parse_arguments() -> argparse.Namespace:
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
        help="Specifies the baudrate. Defaults to 57600 which is the eFPGAs baud rate at 10 MHz.",
        type=int,
        default=57600,
    )
    args = parser.parse_args()
    return args


def get_device_port(device_name: str) -> str:
    """Get the device port of a connected device.

    :param device_name: The name of the device to be used, default to ""
    :return: The device port for the specified device name.
    :rtype: str
    """

    device_port = ""
    device_names = []
    found_device = False
    ports = serial.tools.list_ports.comports()

    # Assign the device port if a matching device was found
    for port in ports:
        if device_name != "":
            if device_name in str(port.product):
                device_port = port.device
            if found_device:
                print(
                    colored("Error: ", "red")
                    + f"""Multiple serial devices of type {device_name} found.
       Please connect only one device of this type."""
                )
                exit(1)
            found_device = True
        else:
            device_port = port.device
            device_names.append(port.interface)
            if found_device:
                print(
                    colored("Error: ", "red")
                    + f"""Multiple serial devices found.
       Please either specify the type or connect only one device."""
                )
                _print_device_names(device_names)
                print(
                    """
       It is sufficient to specify the first part of the name:
       E.g. for \"FT232R USB UART\" just specify \"FT232R\"."""
                )
                exit(1)
            found_device = True

    if not found_device:
        print(
            colored("Error: ", "red")
            + f"""No serial device found.
       Please check if a device is connected"""
        )
        exit(1)

    return device_port


def read_bitstream_data(bitstream_file: str) -> bytearray:
    """Read the bitstream data from the specified file.

    :param bitstream_file: The bitstream file to be read.
    :type bitstream_file: str
    :return: The bitstream data read from the file.
    :rtype: bytearray
    """
    file = Path(bitstream_file)
    if not file.is_file():
        print(
            colored("Error: ", "red")
            + f"""File "{bitstream_file}" does not exist.
       Check for spelling and if a bitstream file was created."""
        )
        exit(1)

    with open(bitstream_file, "rb") as f:
        data = bytearray(f.read())

    return data


def _print_device_names(device_names: List) -> None:
    """
    :param device_names: The device names to be printed.
    :type device_names: List
    """
    print("\n       Found the following devices:")
    for device_name in device_names:
        if device_name == None:
            device_name = "<No name specified>"
        print(f"       {device_name}")


def upload_bitstream(bitstream_file: str, baudrate: int, device_port: str = "", device_name: str = "") -> None:
    """Upload the bitstream to the eFPGA.

    :param bitstream_file: The bitstream file to be uploaded.
    :type bitstream_file: str
    :param baudrate: The baudrate to be used for the upload.
    :type baudrate: int
    :param device_port: The port for the serial interface.
    :type device_port: str
    :param device_name: (Optional) name to search for the serial interface.
    :type device_prot: str
    """
    print("Checking device...")

    if device_port == "":
        device_port = get_device_port(device_name)

    data = read_bitstream_data(bitstream_file)
    print("Uploading bitstream...")

    with serial.Serial(device_port, baudrate) as ser:
        ser.write(data)

    print("Bitstream transmitted!")


def main() -> None:
    """The main function containing the application logic"""
    args = parse_arguments()
    upload_bitstream(args.bitstream_file, args.baudrate, args.device_port, args.device_name)


if __name__ == "__main__":
    main()
