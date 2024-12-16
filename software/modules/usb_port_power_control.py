import subprocess
import time
import platform
from shutil import which
from loguru import logger


class OutDatedLinuxKernelVersionError(Exception):
    """An exception to be thrown when the Linux kernel version is too old to be
    used with uhubctl."""


class OnlyLinuxSupportedError(Exception):
    """An exception to be thrown when Linux is the only supported operating
    system for an operation"""


class ProgramNotInstalledError(Exception):
    """An exception to be thrown when a necessary program is not installed"""


def power_cycle_usb_port(location: str, port: str) -> None:
    """Power cycle the specified USB port at the specified location (USB hub).

    :param location: The USB hub on which the port is located.
    :type location: str
    :param port: The port to be power cylced.
    :type port: str
    """
    if which("uhubctl") is not None:
        # Check if the system is Linux
        if platform.system() == "Linux":
            if __check_linux_kernel_version_is_at_least_6():
                logger.info(f"Power cycling port {port} of hub {location}...")
                subprocess.run(
                    ["uhubctl", "-l", location, "-a", "cycle", "-p", port],
                    stdout=subprocess.DEVNULL,
                )
                time.sleep(5)
            else:
                logger.error(
                    "USB port power switching is working reliably only"
                    + " with version 6.0 or later."
                )

                logger.warning(f"You are running {platform.release()}.")
                logger.warning(
                    "Either switch to a newer kernel or power cycle the device"
                    + " manually."
                )
                raise OutDatedLinuxKernelVersionError
        else:
            logger.error("USB port power switching is only supported on Linux.")
            raise OnlyLinuxSupportedError
    else:
        logger.error(
            f"""The program uhubctl is not installed.

   Please install it to be able to reset the board programmatically:
   https://github.com/mvp/uhubctl/tree/master?tab=readme-ov-file
        """
        )
        raise ProgramNotInstalledError


def __check_linux_kernel_version_is_at_least_6() -> bool:
    """Checks if the linux kernel version is a at least 6.x.

    :return: True if the version is at least 6.x, else False.
    :rtype: bool
    """

    # Get the major version number from the kernel release string
    kernel_version = platform.release().split(".")[0]

    try:
        major_version = int(kernel_version)
        return major_version >= 6
    except (IndexError, ValueError):
        return False
