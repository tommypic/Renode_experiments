/* Define the memory regions of the STM32F407 */
MEMORY
{
    FLASH (rx) : ORIGIN = 0x08000000, LENGTH = 1024K
    RAM  (rwx) : ORIGIN = 0x20000000, LENGTH = 128K
}

/* Define the entry point */
ENTRY(main)

SECTIONS
{
    /* The program code goes into FLASH */
    .text :
    {
        KEEP(*(.isr_vector)) /* Keep the interrupt vector table */
        *(.text)             /* All other code */
        *(.rodata)           /* Read-only data */
        . = ALIGN(4);
    } > FLASH

    /* Initialized data goes into RAM, but is stored in FLASH */
    .data : 
    {
        *(.data)
        . = ALIGN(4);
    } > RAM AT > FLASH

    /* Uninitialized data goes into RAM */
    .bss :
    {
        *(.bss)
        *(COMMON)
        . = ALIGN(4);
    } > RAM
}
