#!/usr/bin/env python3

import sys
import re
from typing import List
from pyftdi.ftdi import Ftdi
from io import StringIO


def read_and_check_device_urls(ftdi: Ftdi) -> str:
    """Sets the URL of the connected FTDI device.

    :param ftdi: The FTDI instance to be used.
    :returns: The device URL of the connected FTDI device.
    :rtype: str
    """

    s = StringIO()
    ftdi.show_devices(out=s)

    # Only support 232H devices for now.
    # Other FTDI types might work, but are not tested.
    urls = re.findall(r"(ftdi://ftdi:232h:\S+)", s.getvalue())

    if len(urls) == 0:
        print("Error: No matching FTDI 232H device found!")
        sys.exit(1)
    elif len(urls) > 1:
        print("Warning: Too many FTDI 232H devices connected!")
        __print_device_names(urls)
        # TODO improve
        input_str = input("Type a number to select a device:")
        input_int = int(input_str)
        print("Using FTDI 232H device: " + urls[input_int])
    else:
        print("Found FTDI 232H device: " + urls[0])
    return urls[0]


def __print_device_names(device_names: List) -> None:
    """
    :param device_names: The device names to be printed.
    :type device_names: List
    """
    print("\n       Found the following devices:")
    for device_name in device_names:
        if device_name == None:
            device_name = "<No name specified>"
        print(f"       {device_name}")
