#include <Wire.h>
#include "register_config.h"

#define I2C_ADDRESS 0x60  // Replace with actual I2C address of your device

// Generated using ClockBuilder Pro (https://www.skyworksinc.com/Application-Pages/Clockbuilder-Pro-Software)

// Config for 10 MHz, 25 MHz, 50 MHz
Register config_registers[] = {
  { 0x0002, 0x53 },
  { 0x0003, 0x00 },
  { 0x0004, 0x20 },
  { 0x0007, 0x00 },
  { 0x000F, 0x00 },
  { 0x0010, 0x0F },
  { 0x0011, 0x0F },
  { 0x0012, 0x0F },
  { 0x0013, 0x8C },
  { 0x0014, 0x8C },
  { 0x0015, 0x8C },
  { 0x0016, 0x8C },
  { 0x0017, 0x8C },
  { 0x001A, 0x00 },
  { 0x001B, 0x01 },
  { 0x001C, 0x00 },
  { 0x001D, 0x10 },
  { 0x001E, 0x00 },
  { 0x001F, 0x00 },
  { 0x0020, 0x00 },
  { 0x0021, 0x00 },
  { 0x002A, 0x00 },
  { 0x002B, 0x01 },
  { 0x002C, 0x00 },
  { 0x002D, 0x2B },
  { 0x002E, 0x00 },
  { 0x002F, 0x00 },
  { 0x0030, 0x00 },
  { 0x0031, 0x00 },
  { 0x0032, 0x00 },
  { 0x0033, 0x01 },
  { 0x0034, 0x00 },
  { 0x0035, 0x10 },
  { 0x0036, 0x00 },
  { 0x0037, 0x00 },
  { 0x0038, 0x00 },
  { 0x0039, 0x00 },
  { 0x003A, 0x00 },
  { 0x003B, 0x04 },
  { 0x003C, 0x00 },
  { 0x003D, 0x07 },
  { 0x003E, 0x60 },
  { 0x003F, 0x00 },
  { 0x0040, 0x00 },
  { 0x0041, 0x00 },
  { 0x005A, 0x00 },
  { 0x005B, 0x00 },
  { 0x0095, 0x00 },
  { 0x0096, 0x00 },
  { 0x0097, 0x00 },
  { 0x0098, 0x00 },
  { 0x0099, 0x00 },
  { 0x009A, 0x00 },
  { 0x009B, 0x00 },
  { 0x00A2, 0x00 },
  { 0x00A3, 0x00 },
  { 0x00A4, 0x00 },
  { 0x00A5, 0x00 },
  { 0x00A6, 0x00 },
  { 0x00A7, 0x00 },
  { 0x00B7, 0xD2 },

};

void initial_i2c_sequence();

void setup() {
  initial_i2c_sequence();
}

void loop() {
  // Nothing in the loop for this example
}

void writeToRegister(uint8_t regAddress, uint8_t value) {
  Wire.beginTransmission(I2C_ADDRESS);
  Wire.write(regAddress);
  Wire.write(value);
  Wire.endTransmission();
}

void burstWrite(uint8_t startAddress, uint8_t* data, size_t length) {
  Wire.beginTransmission(I2C_ADDRESS);
  Wire.write(startAddress);
  for (size_t i = 0; i < length; i++) {
    Wire.write(data[i]);
  }
  Wire.endTransmission();
}



void initial_i2c_sequence() {
  Wire.begin();  // Initialize I2C

  // Disable outputs
  writeToRegister(REGISTER_OUTPUT_ENABLE, 0xFF);

  // Power down all output drivers (burst write from REGISTER_CLK0_CONTROL to register 23)
  uint8_t powerDownData[7] = { 0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80 };
  burstWrite(REGISTER_CLK0_CONTROL, powerDownData, 7);

  // Set interrupt masks (write to the first register in the config)
  writeToRegister(config_registers[0].address, config_registers[0].value);

  // Write config to the registers starting after register 3
  for (size_t i = 2; i < REGISTER_COUNT; i++) {
    writeToRegister(config_registers[i].address, config_registers[i].value);
  }

  // Apply PLLA and PLLB soft reset
  writeToRegister(REGISTER_PLL_RESET, 0xAC);

  // Enable outputs for CLK0, CLK1, and CLK2 (write to the second register in the config)
  writeToRegister(config_registers[1].address, config_registers[1].value);
}