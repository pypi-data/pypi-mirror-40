#include <gxx/debug/delay.h>

double __debug_delay_multiplier = 1;

void cpu_delay(uint64_t ticks) {
	volatile uint64_t count = ticks;
	while(count--);
}

void debug_simple_delay(uint64_t ticks) {
	volatile uint64_t count = ticks;
	while(count--);
}

void debug_delay(uint32_t ms) {
	debug_simple_delay(ms * __debug_delay_multiplier);
}