#include "protocol.h"
#include <stdio.h>
#include <string.h>

int vaanicore_encode_frame(uint8_t seq, const char *verb, const char *fields, char *out, size_t capacity) {
  if (!verb || !out || capacity < 7) return -1;
  int body_len = fields && fields[0] ? snprintf(out, capacity, "@%u:%s:%s", seq, verb, fields) : snprintf(out, capacity, "@%u:%s", seq, verb);
  if (body_len < 0 || (size_t)body_len + 6 > capacity || body_len > 123) return -1;
  uint16_t crc = vaanicore_crc16((const uint8_t *)out, (size_t)body_len);
  int total = snprintf(out + body_len, capacity - (size_t)body_len, "%04X\n", crc);
  return total < 0 || (size_t)(body_len + total) > capacity ? -1 : body_len + total;
}
