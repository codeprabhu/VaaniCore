/* ESP-IDF integration skeleton: hardware execution is not claimed in bootstrap. */
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_log.h"
#include "nvs_flash.h"
#include "audio_capture.h"
#include "ui.h"
#include "pins.h"

static const char *TAG = "vaanicore";
static TaskHandle_t audio_handle;
static QueueHandle_t ui_events;
static void audio_task(void *arg) { (void)arg; int16_t samples[256]; size_t count; for (;;) { ulTaskNotifyTake(pdTRUE, portMAX_DELAY); vaanicore_audio_read(samples, 256, &count); } }
static void idle_task(void *arg) { (void)arg; for (;;) { vTaskDelay(pdMS_TO_TICKS(50)); } }
static void ui_task(void *arg) { (void)arg; vc_ui_event_t event; for (;;) { if (xQueueReceive(ui_events, &event, portMAX_DELAY) == pdTRUE) { (void)event; } } }

void app_main(void) {
  nvs_flash_init();
  ui_events = xQueueCreate(8, sizeof(vc_ui_event_t));
  vaanicore_ui_init(ui_events);
  ESP_LOGI(TAG, "VaaniCore scaffold: I2S=%d/%d/%d USB=%d/%d", PIN_I2S_BCLK, PIN_I2S_WS, PIN_I2S_DIN, PIN_USB_DM, PIN_USB_DP);
  xTaskCreatePinnedToCore(audio_task, "audio_task", 4096, NULL, 6, &audio_handle, 0);
  xTaskCreatePinnedToCore(idle_task, "dsp_task", 4096, NULL, 5, NULL, 1);
  xTaskCreatePinnedToCore(idle_task, "infer_task", 4096, NULL, 4, NULL, 1);
  xTaskCreatePinnedToCore(idle_task, "intent_task", 3072, NULL, 3, NULL, 1);
  xTaskCreatePinnedToCore(idle_task, "context_task", 3072, NULL, 2, NULL, 1);
  xTaskCreatePinnedToCore(idle_task, "comms_task", 4096, NULL, 4, NULL, 0);
  xTaskCreatePinnedToCore(ui_task, "ui_task", 3072, NULL, 2, NULL, 1);
  xTaskCreatePinnedToCore(idle_task, "power_task", 3072, NULL, 1, NULL, 1);
  vaanicore_audio_init(audio_handle);
}
