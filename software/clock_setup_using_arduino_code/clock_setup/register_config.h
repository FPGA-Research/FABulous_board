#ifndef CONFIG_REGISTERS_H
#define CONFIG_REGISTERS_H

#include <stdint.h>

typedef struct {
  uint8_t address;
  uint8_t value;
} Register;

extern Register config_registers[];

#define REGISTER_COUNT (sizeof(config_registers) / sizeof(config_registers[0]))
#define REGISTER_OUTPUT_ENABLE 3u
#define REGISTER_CLK0_CONTROL 16u
#define REGISTER_PLL_RESET 177u
#define REGISTER_CRYSTAL_INTERNAL_LOAD_CAPACITANCE 183u

#endif // CONFIG_REGISTERS_H
