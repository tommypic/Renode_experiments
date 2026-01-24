# Toolchain definition
CC = arm-none-eabi-gcc
OBJCOPY = arm-none-eabi-objcopy

# Project files
TARGET = blink
SRCS = main.c
LINKER_SCRIPT = stm32f4.ld

# Compiler flags
# -mcpu=cortex-m4: target the STM32F4 processor
# -mthumb: use the Thumb instruction set
# -nostdlib: do not use standard C libraries (minimalist approach)
CFLAGS = -mcpu=cortex-m4 -mthumb -Wall -g -nostdlib
LDFLAGS = -T $(LINKER_SCRIPT)

all: $(TARGET).elf

$(TARGET).elf: $(SRCS)
	$(CC) $(CFLAGS) $(LDFLAGS) $(SRCS) -o $(TARGET).elf
	@echo "Build Successful: $(TARGET).elf"

clean:
	rm -f $(TARGET).elf
