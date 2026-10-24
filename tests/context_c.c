#include "context.h"
#include <stdio.h>
#include <string.h>

int main(void) {
  vc_history_t history; vc_event_t result;
  vc_history_init(&history);
  vc_history_append(&history, "filter", "OPEN_PROJECT", 100);
  vc_history_append(&history, "amplifier", "RUN_SIMULATION", 101);
  if (!vc_history_resolve(&history, "LAST", 101, &result) || strcmp(result.project_id, "amplifier") != 0) return 1;
  if (!vc_history_resolve(&history, "YESTERDAY", 101, &result) || strcmp(result.project_id, "filter") != 0) return 1;
  puts("C context vectors passed"); return 0;
}
