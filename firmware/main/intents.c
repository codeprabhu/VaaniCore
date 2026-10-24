#include "intents.h"
#include <string.h>

static const vc_intent_t INTENTS[] = {
    {"open_amplifier", "OPEN_PROJECT", "amplifier", 0, 0},
    {"open_filter", "OPEN_PROJECT", "filter", 0, 0},
    {"open_regulator", "OPEN_PROJECT", "regulator", 0, 0},
    {"open_last", "OPEN_PROJECT", "LAST", 0, 0},
    {"open_yesterday", "OPEN_PROJECT", "YESTERDAY", 0, 0},
    {"run_sim", "RUN_SIMULATION", "LAST", 0, 0},
    {"open_amp_run_sim", "RUN_SIMULATION", "amplifier", 0, 1},
    {"open_yday_run_sim", "RUN_SIMULATION", "YESTERDAY", 0, 1},
    {"show_result", "SHOW_RESULT", "LAST", 0, 0},
    {"cancel", "CANCEL", "", 0, 0},
    {"confirm", "CONFIRM", "", 0, 0},
    {"close_project", "CLOSE_PROJECT", "LAST", 1, 0},
    {"_unknown_", "", "", 0, 0},
    {"_silence_", "", "", 0, 0},
};

const vc_intent_t *vc_intent_lookup(const char *class_name) {
  if (!class_name) return NULL;
  for (size_t i = 0; i < sizeof(INTENTS) / sizeof(INTENTS[0]); ++i) {
    if (strcmp(INTENTS[i].class_name, class_name) == 0) return &INTENTS[i];
  }
  return NULL;
}

size_t vc_intent_count(void) { return sizeof(INTENTS) / sizeof(INTENTS[0]); }
