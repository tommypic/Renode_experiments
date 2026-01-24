#include <stdint.h>

// Memory addresses for STM32F4 Discovery (from technical manual)
#define RCC_AHB1ENR (*(volatile uint32_t *)(0x40023830))
#define GPIOD_MODER (*(volatile uint32_t *)(0x40020C00))
#define GPIOD_ODR (*(volatile uint32_t *)(0x40020C14))
// Minimal Vector Table

void delay(int count) {
  for (int i = 0; i < count; i++) {
    __asm__("nop"); // Simple delay loop
  }
}

int main(void) {
  // 1. Enable clock for GPIOD (Port D)
  RCC_AHB1ENR |= (1 << 3);

  // 2. Set Pin 12 (Green LED) as output
  GPIOD_MODER |= (1 << (12 * 2));

  while (1) {
    GPIOD_ODR ^= (1 << 12); // Toggle LED
    delay(10000000);
  }
}

__attribute__((section(".isr_vector"))) uint32_t *vectors[] = {
    (uint32_t *)0x20020000, // Initial Stack Pointer
    (uint32_t *)main        // Reset Handler (Start here)
};
