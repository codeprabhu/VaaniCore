#pragma once
#include <stddef.h>
#include <stdint.h>

#define VAANICORE_MAX_FRAME 128
#define VAANICORE_MAX_VERB 31
#define VAANICORE_MAX_FIELDS 95

typedef struct {
  uint8_t seq;
  char verb[VAANICORE_MAX_VERB + 1];
  char fields[VAANICORE_MAX_FIELDS + 1];
} vaanicore_frame_t;

uint16_t vaanicore_crc16(const uint8_t *data, size_t length);
int vaanicore_encode_frame(uint8_t seq, const char *verb, const char *fields, char *out, size_t capacity);
int vaanicore_decode_frame(const char *line, size_t length, vaanicore_frame_t *out);
