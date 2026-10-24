#include "intents.h"
#include <stdio.h>
#include <string.h>

int main(void) {
  const vc_intent_t *run = vc_intent_lookup("open_amp_run_sim");
  const vc_intent_t *close = vc_intent_lookup("close_project");
  if (vc_intent_count() != 14 || !run || strcmp(run->verb, "RUN_SIMULATION") != 0 || !run->open_before_run) return 1;
  if (!close || !close->risky || vc_intent_lookup("not_a_class") != NULL) return 1;
  puts("C intent table passed");
  return 0;
}
