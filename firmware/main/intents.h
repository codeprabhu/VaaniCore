#pragma once

#include <stddef.h>

typedef struct {
  const char *class_name;
  const char *verb;
  const char *project;
  int risky;
  int open_before_run;
} vc_intent_t;

const vc_intent_t *vc_intent_lookup(const char *class_name);
size_t vc_intent_count(void);
