/* ESP-IDF integration skeleton: hardware execution is not claimed in bootstrap. */
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_log.h"
#include "nvs_flash.h"
#include "pins.h"

static const char *TAG = "vaanicore";
static void audio_task(void *arg) { (void)arg; for (;;) { vTaskDelay(pdMS_TO_TICKS(16)); } }
static void dsp_task(void *arg) { (void)arg; for (;;) { vTaskDelay(pdMS_TO_TICKS(16)); } }
static void comms_task(void *arg) { (void)arg; for (;;) { vTaskDelay(pdMS_TO_TICKS(50)); } }

void app_main(void) {
  nvs_flash_init();
  ESP_LOGI(TAG, "VaaniCore scaffold: I2S=%d/%d/%d USB=%d/%d", PIN_I2S_BCLK, PIN_I2S_WS, PIN_I2S_DIN, PIN_USB_DM, PIN_USB_DP);
  xTaskCreatePinnedToCore(audio_task, "audio_task", 4096, NULL, 6, NULL, 0);
  xTaskCreatePinnedToCore(dsp_task, "dsp_task", 4096, NULL, 5, NULL, 1);
  xTaskCreatePinnedToCore(comms_task, "comms_task", 4096, NULL, 4, NULL, 0);
}
