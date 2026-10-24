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
  puts("C protocol vector passed");
  return 0;
}
