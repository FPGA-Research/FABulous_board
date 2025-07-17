# How to setup and upload code

To flash the firmware for configuring the PLL chip to compatible MCUs we will be using the [Arduino-CLI](https://github.com/arduino/arduino-cli).

## Procedure

### Prerequisite

- Install `libhidapi-hidraw0` library for USB serial communication.
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install libhidapi-hidraw0
```

### Install Arduino CLI
- Move to directory `./software/clock_setup_using_arduino_code` which contains the Makefile required for setup, compilation and uploading the sketch.
```bash
# install Arduino CLI

# NOTE: the CLI will be installed in the $PATH_INSTALL provided.
# Default path: ~/arduino_cli

make setup-arduino-cli PATH_INSTALL=<installation_path>
```
- Once installation is complete add the following line in your `.bashrc` or `.zshrc` to update the `$PATH` variable.
```bash
# When using custom install path
export PATH=<installation_path>/bin:$PATH

# When using default install path 
export PATH=$HOME/arduino_cli/bin:$PATH
```
- Source your `.bashrc` or `.zshrc` after updating `$PATH`.
- Verify your installation.

```bash
# arduino CLI installation path
which arduino-cli

# arduino CLI installed version
arduino-cli version
```

### Install Board Files
- Now we need to setup and add the board support files for our CH32 EVT chips which can be found [here](https://github.com/openwch/arduino_core_ch32).
- Run `make setup-board-files` which will download, search and install all board files necessary.

### Compile and Upload
- Now connect the chip using the WCH-Debugger Link and run the following command:
  ```bash
  # show all connected boards/chips via USB
  make list-boards
  ```
- Make sure to check if the port e.g. `/dev/ttyACM0` is the same as in the `Makefile`. If not, update it accordingly.
- To compile the sketch run:
  ```bash
  make compile
  ```
- To upload the sketch on the chip run:
  ```bash
  make upload
  ```
