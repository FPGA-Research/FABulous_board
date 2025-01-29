# How to setup and upload code

To flash the firmware for configuring the PLL chip to compatible MCUs we will be using [Arduino-CLI](https://github.com/arduino/arduino-cli).

## Procedure

### Prerequisite

- Add the following line in your `.bashrc` or `.zshrc`.
```bash
export PATH=$HOME/arduino_cli/bin:$PATH
```
- Make sure to source your `.bashrc` or `.zshrc` after updating `$PATH`.

- Install `libhidapi-hidraw0` library for USB serial communication.
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install libhidapi-hidraw0
```

### Install Arduino CLI
- Move to directory `./software/clock_setup_using_arduino_code` which contains
the Makefile required for setup, compilation and uploading the sketch.
- Run `make setup-arduino-cli` which will install `arduino-cli`.

### Install Board Files
- Now we need to setup and add the board support files for our CH32 EVT chips which can be found [here](https://github.com/openwch/arduino_core_ch32).
- Run `make setup-board-files` which will download, search and install all board files necessary.

### Compile and Upload
- Now connect the chip using the WCH-Debugger Link and run the following command:
  ```bash
  # show all connected boards/chips via USB
  make list-boards
  ```
- Make sure to check if Port value e.g. `/dev/ttyACM0` is the same as in the `Makefile`. If not, update it accordingly.
- To compile the sketch run:
  ```bash
  make compile
  ```
- To upload the sketch on the chip run:
  ```bash
  make upload
  ```
