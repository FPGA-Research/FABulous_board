#!/usr/bin/env python3

import serial
import serial.tools.list_ports
from typing import NamedTuple, List
from pyftdi.ftdi import UsbDeviceDescriptor
from pyftdi.usbtools import UsbTools
from loguru import logger
import inquirer
import pyudev
import os
import re
from collections import namedtuple

# Define a named tuple to store bus and port values
USBTopology = namedtuple('USBTopology', ['bus', 'port'])

DEFAULT_FTDI_ID = "0403:6014"
INQUIRER_LIST_NAME = "Device"

class MultipleDevicesError(Exception):
    """An exception to be thrown when multiple devices are connected and cannot
    be distinguished."""


class NoDeviceFoundError(Exception):
    """An exception to be thrown when no device was found."""


class NoDeviceArgument(Exception):
    """An exception to be thrown when no device was given as an argument."""


class Device(NamedTuple):
    vendor_id: int
    product_id: int


def select_specific_device(device_id: str) -> str:
    """Select a specific FTDI device

    :param vendor_id: The device ID.
    :type vendor_id: str
    :return: The FTDI URL of the selected device.
    :rtype: str
    :raises ValueError: If no device was selected.
    """
    url = None
    matching_devices = find_devices_matching_id(device_id)

    if len(matching_devices) > 1:
        selected_device = select_device(matching_devices)
        if selected_device is not None:
            url = __build_device_url(selected_device)
        else:
            raise ValueError
    else:
        selected_device = matching_devices[0]
        url = __build_device_url(selected_device)
        logger.info(f"Selected URI: {url}")

    return url


def find_devices_matching_id(device_id: str) -> List[UsbDeviceDescriptor]:
    """Find all devices with IDs matching the given device ID.

    :param device_id: The device ID for which to find matching devices.
    :type device_id: str
    :return: All devices matching the device ID.
    :rtype: List[UsbDeviceDescriptor]
    :raises NoDeviceFoundError: If no matching device was found.
    """
    vendor_id, product_id = __extract_vendor_and_product_id_from_device_id(device_id)
    matching_devices = []
    # Find all FTDI devices
    devices = UsbTools.find_all([(vendor_id, product_id)])

    # Filter devices by VID and PID
    for dev, _ in devices:
        if dev.vid == vendor_id and dev.pid == product_id:
            matching_devices.append(dev)

    # Check if any matching devices were found
    if not matching_devices:
        logger.error(
            f"No devices found with VID {vendor_id:04x} and PID"
            + f" {product_id:04x}. Please check the specified IDs, the"
            + f" connection and the board."
        )
        raise NoDeviceFoundError

    # Sort the devices
    matching_devices.sort(key=lambda dev: (dev.vid, dev.pid, dev.address))
    return matching_devices


def select_device(devices: List[UsbDeviceDescriptor]) -> UsbDeviceDescriptor:
    """Select a device from a list of devices.

    :param devices: The list of devices where to select a device from.
    :type devices: List[UsbDeviceDescriptor]
    :return: The selected device.
    :rtype: UsbDeviceDescriptor
    :raises NoDeviceArgument: If no devices were given as an argument.
    :raises ValueError: If no device was selected.
    :raises KeyboardInterrupt: If the selection is canceled by the user.
    """
    selected_device = None
    if len(devices) == 0:
        logger.error("No devices given for selection.")
        raise NoDeviceArgument
    elif len(devices) == 1:
        selected_device = devices[0]
    else:
        device_list = []
        for index, dev in enumerate(devices):
            device = (
                f"{index}: Vendor ID: {dev.vid:04x}, Product ID: {dev.pid:04x},"
                + f" Address: {dev.address}, Description: {dev.description}"
            )
            device_list.append(device)

        selectable_devices = [
            inquirer.List(
                INQUIRER_LIST_NAME,
                message="Please select a device:",
                choices=device_list,
            )
        ]
        selected_device = inquirer.prompt(
            selectable_devices, raise_keyboard_interrupt=True
        )
        if selected_device is not None:
            # The index is the first character
            selected_index = int(selected_device[INQUIRER_LIST_NAME][0])
            selected_device = devices[selected_index]
        else:
            raise ValueError
    return selected_device


def get_single_device(device_id: str) -> UsbDeviceDescriptor:
    """Get a single device for the given device ID.

    :param device_id: The device ID for which to get a single device.
    :type device_id: str
    :return: The single selected device.
    :rtype: UsbDeviceDescriptor
    :raises ValueError: If no devices matching the ID were found.
    """
    selected_device = None
    devices = find_devices_matching_id(device_id)
    if devices is not None:
        selected_device = select_device(devices)
    else:
        raise ValueError
    return selected_device


def get_device_url(device_id: str) -> str:
    """Get the URL for a given device ID
    :param device_id: The device ID for which to get the device URL.
    :type device_id: str
    :return The URL for the given device ID:
    :rtype: str
    :raises ValueError: If no device was found.
    """
    device = get_single_device(device_id)
    url = None
    if device is not None:
        url = __build_device_url(device)
    else:
        raise ValueError
    return url


def get_device_path_for_device_id(device_id: str) -> str | None:
    """Get the device path for a given device ID

    :param device_id: The ID of a device to get the path for. 
    :type device_id: str
    :return: The device path of a single selected device matching the given
    device ID.
    :type: str | None
    :raises ValueError: If no device with the given device ID was found.
    """
    device_path = None
    device = get_single_device(device_id)
   
    if device != None:
        if device.address != None:
            device_path = get_path_for_address(device.address)
    else:
        raise ValueError
    return device_path

def get_path_for_address(address: int) -> str | None:
    """
    Check  if the given path is the correct path for the given address.

    :return: True if the given path is the correct path for the given address,
    else False.
    """
    context = pyudev.Context()

    device_path = None
    for device in context.list_devices(subsystem="tty"):
        # Extract the USB bus/port topology from the parent's device_path
        usb_topology = extract_bus_and_port_from_full_path(device.properties.device.device_path)
        if usb_topology is not None:
            device_number = get_device_number_from_topology(usb_topology.bus,
                                                     usb_topology.port)
            if device_number == address:
                device_path = device.device_node  # e.g., "/dev/ttyUSB0"
    return device_path

def extract_bus_and_port_from_full_path(path: str) -> USBTopology | None:
    """
    Extract port and address values from a USB device path.
    
    :param path: The USB device path string.
    :return: A tuple (port, address) as integers, or None if not found.
    """
    match = re.search(r'/usb(\d+)/(\d+)-(\d+)', path)
    if match:
        bus, port = match.group(2), match.group(3)
        return USBTopology(bus=bus, port=port)
    return None

def get_device_number_from_topology(bus: str, port: str) -> int | None:
    """
    Translate USB topology (bus-port, e.g., '1-3') to the dynamic device number.
    :param bus: USB bus number as a string (e.g., "1").
    :param port: USB topology path (e.g., "1-3").
    :return: The dynamic device number (e.g., "5"), or None if not found.
    :rtype: int
    """
    usb_base_path = "/sys/bus/usb/devices"

    # Topology path as it would appear under /sys/bus/usb/devices (e.g., "1-3")
    topology_path = f"{bus}-{port}"

    # Full path to the device in the USB sysfs tree
    full_path = os.path.join(usb_base_path, topology_path)

    if os.path.exists(full_path):
        try:
            # Read the dynamic device number (devnum) from the device attributes
            with open(os.path.join(full_path, "devnum"), "r") as f:
                device_number = int(f.read().strip())
            return device_number
        except FileNotFoundError:
            return None
    return None

def __extract_vendor_and_product_id_from_device_id(device_id: str) -> NamedTuple:
    """Extract the vendor and product ID from the device ID.

    :param device_id: The device ID where to extract the vendor and product ID
    from.
    :type device_id: str
    :return: The extracted vendor and device ID.
    :rtype: Tuple[int, int]
    """
    vendor_id = int(device_id.split(":")[0], 16)
    product_id = int(device_id.split(":")[1], 16)
    return Device(vendor_id, product_id)


def __build_device_url(device: UsbDeviceDescriptor) -> str:
    """Get the device URL from the USB device

    :param device: The device to get the URL for.
    :type device: UsbDeviceDescriptor
    :return: The device URL.
    :rtype: str
    """
    device_url = f"ftdi://0x{device.vid:04x}:0x{device.pid:04x}:0x{device.bus:x}:0x{device.address:x}/1"
    return device_url


if __name__ == "__main__":
    pass
