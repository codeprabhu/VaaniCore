#include "context.h"
#include <string.h>

static const vc_event_t *at(const vc_history_t *history, size_t logical) {
  size_t oldest = history->count == VAANICORE_HISTORY_CAPACITY ? history->next : 0;
  return &history->events[(oldest + logical) % VAANICORE_HISTORY_CAPACITY];
}

void vc_history_init(vc_history_t *history) { memset(history, 0, sizeof(*history)); }

void vc_history_append(vc_history_t *history, const char *project_id, const char *action, int32_t local_day) {
  vc_event_t *event = &history->events[history->next];
  memset(event, 0, sizeof(*event));
  strncpy(event->project_id, project_id ? project_id : "", sizeof(event->project_id) - 1);
  strncpy(event->action, action ? action : "", sizeof(event->action) - 1);
  event->local_day = local_day;
  history->next = (history->next + 1) % VAANICORE_HISTORY_CAPACITY;
  if (history->count < VAANICORE_HISTORY_CAPACITY) history->count++;
}

static int resolve_internal(const vc_history_t *history, const char *selector, int32_t today, vc_event_t *out, int confirmed_fallback) {
  if (!history || !selector || !out || history->count == 0) return 0;
  if (strcmp(selector, "LAST") == 0) { *out = *at(history, history->count - 1); return 1; }
  if (strcmp(selector, "YESTERDAY") == 0) {
    int found = 0;
    for (size_t i = history->count; i > 0; --i) {
      const vc_event_t *event = at(history, i - 1);
      if (event->local_day == today - 1) { if (found) return 0; *out = *event; found = 1; }
    }
    if (found) return 1;
    if (confirmed_fallback) { *out = *at(history, history->count - 1); return 1; }
    return 0;
  }
  return 0;
}

int vc_history_resolve(const vc_history_t *history, const char *selector, int32_t today, vc_event_t *out) {
  return resolve_internal(history, selector, today, out, 0);
}

int vc_history_resolve_confirmed(const vc_history_t *history, const char *selector, int32_t today, vc_event_t *out) {
  return resolve_internal(history, selector, today, out, 1);
}
