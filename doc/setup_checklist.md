# Board Setup Checklist

This is a checklist containing all things that turned out to be important during
the chip bring-up and testing, even though some steps seem trivial. The first
group only has to be checked if the correct firmware has not been flashed to the 
board and can be skipped otherwise. Feel free to extend this list if you find
more things to be considered.

## Flashing the Firmware
- Change the chip (if another one should be used/tested)
- Use the correct `gpio_config_io.py`
- Use the correct firmware
- Use the correct `PART` when flashing the firmware
- Use the correct `SHUTTLE` (currently `MPW2` and `MPW5` are supported) when flashing the firmware
- Flash the firmware

## Uploading a User Design
- Check the top wrapper
- Check the user design for bugs
- The `oeb` value should be set to `1` for outputs and `0` for inputs per pin
- Create the bitstream
- Use correct bitstream (link to correct file or select correct file)
- Check for the clock
- Check the baud rate
- Upload the bitstream
  -  for MPW-5: unplug the board and directly reconnect it (due to `oeb`
  misconfiguration in the fabric itself and the type of hold time violation at
  these pins)

## Setting the Jumpers
If the jumpers on your board are not set already, set them as follows:
- `J6`: Connect eFPGA Rx and FTDI Tx
- `J5`: Set for uploading a bitstream, unset for uploading the Caravel firmware
- `J8`: Set the desired clock output of the PLL
- `J4`: Set the desired Voltage
- `J11` and `J13` set the desired internal clock
- `J2` and `J3`: Connect `mprj_io[36]/[37]` either to the Bitbang inputs of the fabric or to pins `22`/`23` of `J7`, depending on your use case (most likely you want to use `22`/`23`)
