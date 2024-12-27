# FABulous board

The PCB created here is used for eFPGAs created using [FABulous](https://github.com/FPGA-Research-Manchester/FABulous]).
It is based on the [hardware files of the caravel board repository](https://github.com/efabless/caravel_board/tree/main/hardware)
at [Commit 1f99718](https://github.com/efabless/caravel_board/commit/1f99718c0766020aeabb0c0db4c8623b71fb3e77)
and was customized to better fit the exact eFPGA pin configuration.

<img src="./doc/img/fabulous_board.jpg" alt="The FABulous board" width="600" height="390">

## Project structure

* `hardware` : Files related to the hardware, like schematics,
  board layout and also simulation files.
* `software` : Files related to the software needed for eFPGA operation, like
uploading the bitstream.
* `doc`: Files related to the project documentation.

## Board Features

* Compatible to all eFPGAs using the [caravel harness](https://github.com/efabless/caravel/tree/main).
* Three adjustable voltage levels for the core voltage :
  * 1.45V
  * 1.6V
  * 1.8V

  &nbsp;&rarr; some boards have just a
  fixed voltage of 1.5V since a fixed instead of an adjustable LDO was used when
  the boards were manufactured.
* Up to 24 IO pins usable for the eFPGA:

    &nbsp;&rarr; depending on how many pins can be
  successfully configured for each chip and how the bitstream will be uploaded.

* Independently configurable clock speeds for SoC and eFPGA.

### Clock selection

There are two types of clock selections on the board. One is the selection
between an external clock, the internal wishbone clock, and a so-called user
clock. The external clock is connected to another jumper that will be explained
later. The wishbone clock is the same clock that is also used by the Caravel
SoC. The user clock effectively is the same clock as the wishbone clock.
These clocks can be selected by setting `CLK_SEL_0` and `CLK_SEL_1` in the
following way:

| CLK_SEL_0 | CLK_SEL_1 | Clock Source        |
|-----------|-----------|---------------------|
|  0        |  X        | external (`J8`)     |
|  1        |  0        | wishbone            |
|  1        |  1        | user                |

The other clock selection is the jumper `J8`, where two different clocks can be
selected. The clocks depend on the configuration of the SI5351A-B-GTR clock chip
and is only in effect if the external clock is used as the clock source shown in
the above table.

## Errata

The first fabricated version of the board ([v0.1](https://github.com/FPGA-Research/FABulous_board/releases/tag/v0.1)) has the following issues:

* `S_DATA` and `S_CLK` are interchanged
* Fixed 1.5V instead of an adjustable LDO
* The used clock chip does not have a persistent configuration. It has to be
reconfigured after each power-up. The current most practical solution is to use
a cheap RISC-V microcontroller which configures the chip. An according Arduino
script can be found in
[software/clock_setup_using_arduino_code/clock_setup/](./software/clock_setup_using_arduino_code/clock_setup/).
