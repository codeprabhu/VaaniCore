#pragma once
#include <stddef.h>
#include <stdint.h>

uint16_t vaanicore_crc16(const uint8_t *data, size_t length);
int vaanicore_encode_frame(uint8_t seq, const char *verb, const char *fields, char *out, size_t capacity);
