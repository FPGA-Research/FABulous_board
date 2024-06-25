# FABulous board

The PCB created here is used for an eFPGA created using the [FABulous Framework](https://github.com/FPGA-Research-Manchester/FABulous]).
It is based on the [hardware files of the caravel board repository](https://github.com/efabless/caravel_board/tree/main/hardware)
(commit `1f99718c0766020aeabb0c0db4c8623b71fb3e77`).
The WCSP version is used since the available chips use this package.

## Project structure

* `hardware` : Files related to the hardware, like schematics,
  board layout and also simulation files.
* `software` : Files related to the software needed for eFPGA operation.
  Currently only consists of the UART upload script.

## Board Features

* Compatible with all chips using the [caravel harness](https://github.com/efabless/caravel/tree/main).
* Three adjustable voltage levels for the core voltage:
  * 1.45V
  * 1.6V
  * 1.8V
* Up to 24 IO pins usable for the eFPGA:

    &nbsp;&rarr; depending on how many pins can be
  successfully configured for each chip and how the bitstream will be uploaded.

* Independently configurable clock speeds for SoC and eFPGA.
