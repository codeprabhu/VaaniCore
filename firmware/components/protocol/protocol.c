#include "protocol.h"
#include <ctype.h>
#include <stdlib.h>
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

static int hex_value(char c) {
  if (c >= '0' && c <= '9') return c - '0';
  if (c >= 'A' && c <= 'F') return c - 'A' + 10;
  if (c >= 'a' && c <= 'f') return c - 'a' + 10;
  return -1;
}

int vaanicore_decode_frame(const char *line, size_t length, vaanicore_frame_t *out) {
  if (!line || !out || length < 8 || length > VAANICORE_MAX_FRAME || line[0] != '@' || line[length - 1] != '\n') return -1;
  size_t body_len = length - 5;
  int h0 = hex_value(line[body_len]);
  int h1 = hex_value(line[body_len + 1]);
  int h2 = hex_value(line[body_len + 2]);
  int h3 = hex_value(line[body_len + 3]);
  if (h0 < 0 || h1 < 0 || h2 < 0 || h3 < 0) return -1;
  uint16_t expected = (uint16_t)((h0 << 12) | (h1 << 8) | (h2 << 4) | h3);
  if (vaanicore_crc16((const uint8_t *)line, body_len) != expected) return -2;

  size_t colon = 0;
  for (size_t i = 1; i < body_len; ++i) {
    if (line[i] == ':') { colon = i; break; }
    if (!isdigit((unsigned char)line[i])) return -1;
  }
  if (colon <= 1 || colon >= body_len - 1 || colon - 1 > 3) return -1;
  char seq_buf[4] = {0};
  memcpy(seq_buf, line + 1, colon - 1);
  char *end = NULL;
  unsigned long seq = strtoul(seq_buf, &end, 10);
  if (!end || *end != '\0' || seq > 255) return -1;

  size_t verb_end = colon + 1;
  while (verb_end < body_len && line[verb_end] != ':') ++verb_end;
  size_t verb_len = verb_end - colon - 1;
  if (verb_len == 0 || verb_len > VAANICORE_MAX_VERB) return -1;
  for (size_t i = 0; i < verb_len; ++i) {
    unsigned char c = (unsigned char)line[colon + 1 + i];
    if (!(isalnum(c) || c == '_')) return -1;
  }
  memcpy(out->verb, line + colon + 1, verb_len);
  out->verb[verb_len] = '\0';
  out->seq = (uint8_t)seq;
  out->fields[0] = '\0';
  if (verb_end < body_len) {
    size_t fields_len = body_len - verb_end - 1;
    if (fields_len > VAANICORE_MAX_FIELDS) return -1;
    memcpy(out->fields, line + verb_end + 1, fields_len);
    out->fields[fields_len] = '\0';
  }
  return 0;
}
