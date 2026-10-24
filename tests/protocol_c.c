#include "protocol.h"
#include <stdio.h>
#include <string.h>

int main(void) {
  char frame[128];
  int length = vaanicore_encode_frame(1, "PING", "", frame, sizeof(frame));
  const char *expected = "@1:PINGECA9\n";
  if (length != (int)strlen(expected) || strcmp(frame, expected) != 0) {
    fprintf(stderr, "got %s", frame); return 1;
  }
  vaanicore_frame_t decoded;
  if (vaanicore_decode_frame(frame, strlen(frame), &decoded) != 0 || decoded.seq != 1 ||
      strcmp(decoded.verb, "PING") != 0 || decoded.fields[0] != '\0') return 1;
  const char *with_fields = "@2:RUN_SIMULATION:project=amplifierDDCD\n";
  if (vaanicore_decode_frame(with_fields, strlen(with_fields), &decoded) != 0 || decoded.seq != 2 ||
      strcmp(decoded.verb, "RUN_SIMULATION") != 0 || strcmp(decoded.fields, "project=amplifier") != 0) return 1;
  char corrupted[128];
  memcpy(corrupted, with_fields, strlen(with_fields));
  corrupted[10] = 'X';
  if (vaanicore_decode_frame(corrupted, strlen(with_fields), &decoded) != -2) return 1;
  if (vaanicore_decode_frame("@1:PING0000\n", 12, &decoded) != -2) return 1;
  if (vaanicore_decode_frame("@1:PING\n", 8, &decoded) != -1) return 1;
  puts("C protocol vector passed");
  return 0;
}
