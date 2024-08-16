/*
  * Copyright (c) 2020 Raspberry Pi (Trading) Ltd.
  *
  * SPDX-License-Identifier: BSD-3-Clause
  */
  
 #ifndef _PICO_STDLIB_H
 #define _PICO_STDLIB_H
  
 #include "pico.h"
 #include "pico/stdio.h"
 #include "pico/time.h"
 #include "hardware/gpio.h"
 #include "hardware/uart.h"
  
 #ifdef __cplusplus
 extern "C" {
 #endif
  
 // Note PICO_STDIO_UART, PICO_STDIO_USB, PICO_STDIO_SEMIHOSTING are set by the
 // respective INTERFACE libraries, so these defines are set if the library
 // is included for the target executable
  
 #if LIB_PICO_STDIO_UART
 #include "pico/stdio_uart.h"
 #endif
  
 #if LIB_PICO_STDIO_USB
 #include "pico/stdio_usb.h"
 #endif
  
 #if LIB_PICO_STDIO_SEMIHOSTING
 #include "pico/stdio_semihosting.h"
 #endif
  
 // PICO_CONFIG: PICO_DEFAULT_LED_PIN, Optionally define a pin that drives a regular LED on the board, group=pico_stdlib
  
 // PICO_CONFIG: PICO_DEFAULT_LED_PIN_INVERTED, 1 if LED is inverted or 0 if not, type=int, default=0, group=pico_stdlib
 #ifndef PICO_DEFAULT_LED_PIN_INVERTED
 #define PICO_DEFAULT_LED_PIN_INVERTED 0
 #endif
  
 // PICO_CONFIG: PICO_DEFAULT_WS2812_PIN, Optionally define a pin that controls data to a WS2812 compatible LED on the board, group=pico_stdlib
 // PICO_CONFIG: PICO_DEFAULT_WS2812_POWER_PIN, Optionally define a pin that controls power to a WS2812 compatible LED on the board, group=pico_stdlib
  
 void setup_default_uart(void);
  
 void set_sys_clock_48mhz(void);
  
 void set_sys_clock_pll(uint32_t vco_freq, uint post_div1, uint post_div2);
  
 bool check_sys_clock_khz(uint32_t freq_khz, uint *vco_freq_out, uint *post_div1_out, uint *post_div2_out);
  
 static inline bool set_sys_clock_khz(uint32_t freq_khz, bool required) {
     uint vco, postdiv1, postdiv2;
     if (check_sys_clock_khz(freq_khz, &vco, &postdiv1, &postdiv2)) {
         set_sys_clock_pll(vco, postdiv1, postdiv2);
         return true;
     } else if (required) {
         panic("System clock of %u kHz cannot be exactly achieved", freq_khz);
     }
     return false;
 }
  
 #ifdef __cplusplus
 }
 #endif
 #endif