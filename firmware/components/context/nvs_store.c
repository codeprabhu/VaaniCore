#include "nvs_store.h"
#include "nvs.h"
#include <string.h>

#define NVS_NAMESPACE "vaanicore"
#define NVS_KEY "history"

int vc_history_load_nvs(vc_history_t *history) {
  nvs_handle_t handle;
  vc_history_init(history);
  if (nvs_open(NVS_NAMESPACE, NVS_READONLY, &handle) != ESP_OK) return 0;
  size_t size = sizeof(*history);
  esp_err_t result = nvs_get_blob(handle, NVS_KEY, history, &size);
  nvs_close(handle);
  if (result != ESP_OK || size != sizeof(*history) || history->count > VAANICORE_HISTORY_CAPACITY || history->next >= VAANICORE_HISTORY_CAPACITY) {
    vc_history_init(history); return 0;
  }
  return 1;
}

int vc_history_save_nvs(const vc_history_t *history) {
  nvs_handle_t handle;
  if (!history || history->count > VAANICORE_HISTORY_CAPACITY || history->next >= VAANICORE_HISTORY_CAPACITY) return 0;
  if (nvs_open(NVS_NAMESPACE, NVS_READWRITE, &handle) != ESP_OK) return 0;
  esp_err_t result = nvs_set_blob(handle, NVS_KEY, history, sizeof(*history));
  if (result == ESP_OK) result = nvs_commit(handle);
  nvs_close(handle);
  return result == ESP_OK;
}
