#include <gxx/panic.h>
#include <stdlib.h>

void panic(const char* str) {
	dprln(str);
	abort();
}