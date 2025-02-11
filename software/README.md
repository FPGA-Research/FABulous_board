# Software

## Contents

`clock_setup` : A module to set up the PLL chip on the board. Requires an
additional compatible FTDI adapter.

`clock_setup_using_arduino_code/clock_setup` : An Arduino project quickly set
up to flash a firmware for configuring the PLL chip to compatible microcontrollers. 

`modules` : Different modules needed for the main script.

`upload_bitstream` : Contains a script to upload a bitstream
using the UART protocol.

`board.py` : The main script which provides functionality to interact with the
board. Described in detail below.

## Board CLI

The main functionality of `board.py` is uploading a bitstream over UART to the
board. It was created using `argparse`, so for a full breakdown of the commands
simply use

```console
./board.py -h
```

This is the general usage of the command:

```console
board.py [-h] [-i DEVICE_ID] [-v] {config_clocks,upload} ...
```

Below, the main use cases are given as examples. By default, devices with the VID
`0403` and PID `6014` and a baud rate of 57600 are used.

> [!IMPORTANT]
> Make sure to adjust the files to your local files.


### Main use cases

Uploading a bitstream:

```console
./board.py upload bitstream.bin
```

Configure the PLL clock chip (using an external FTDI adapter):
```console
./board.py config_clocks register_config.txt
```

A configuration file for output clocks of 10MHz, 2MHz and 20MHz for the three
clocks is given in `clock_setup`.






