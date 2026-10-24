#pragma once
#include <stddef.h>
#include <stdint.h>

#define VAANICORE_HISTORY_CAPACITY 16
typedef struct { char project_id[24]; char action[24]; int32_t local_day; } vc_event_t;
typedef struct { vc_event_t events[VAANICORE_HISTORY_CAPACITY]; size_t count; size_t next; } vc_history_t;
void vc_history_init(vc_history_t *history);
void vc_history_append(vc_history_t *history, const char *project_id, const char *action, int32_t local_day);
int vc_history_resolve(const vc_history_t *history, const char *selector, int32_t today, vc_event_t *out);
int vc_history_resolve_confirmed(const vc_history_t *history, const char *selector, int32_t today, vc_event_t *out);
