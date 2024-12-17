# FABulous board

The PCB created here is used for an eFPGA created using [FABulous](https://github.com/FPGA-Research-Manchester/FABulous]).
It is based on the [hardware files of the caravel board repository](https://github.com/efabless/caravel_board/tree/main/hardware) at [Commit 1f99718](https://github.com/efabless/caravel_board/commit/1f99718c0766020aeabb0c0db4c8623b71fb3e77).

## Project structure

* `hardware` : Files related to the hardware, like schematics,
  board layout and also simulation files.
* `software` : Files related to the software needed for eFPGA operation, like
uploading the bitstream.

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
