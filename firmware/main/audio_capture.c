#include "audio_capture.h"
#include "driver/i2s_std.h"
#include "esp_err.h"
#include "esp_heap_caps.h"
#include "pins.h"
#include <stdlib.h>

static i2s_chan_handle_t rx_channel;
static TaskHandle_t audio_notify_task;

static bool IRAM_ATTR on_i2s_receive(i2s_chan_handle_t handle, i2s_event_data_t *event, void *user_ctx) {
  (void)handle; (void)event; (void)user_ctx;
  BaseType_t higher_priority_task_woken = pdFALSE;
  vTaskNotifyGiveFromISR(audio_notify_task, &higher_priority_task_woken);
  return higher_priority_task_woken == pdTRUE;
}

esp_err_t vaanicore_audio_init(TaskHandle_t notify_task) {
  audio_notify_task = notify_task;
  i2s_chan_config_t channel_config = I2S_CHANNEL_DEFAULT_CONFIG(I2S_NUM_0, I2S_ROLE_MASTER);
  channel_config.dma_desc_num = 6;
  channel_config.dma_frame_num = 256;
  esp_err_t err = i2s_new_channel(&channel_config, NULL, &rx_channel);
  if (err != ESP_OK) return err;
  i2s_std_config_t standard_config = {
      .clk_cfg = I2S_STD_CLK_DEFAULT_CONFIG(16000),
      .slot_cfg = I2S_STD_MSB_SLOT_DEFAULT_CONFIG(I2S_DATA_BIT_WIDTH_32, I2S_SLOT_MODE_MONO),
      .gpio_cfg = {.mclk = I2S_GPIO_UNUSED, .bclk = PIN_I2S_BCLK, .ws = PIN_I2S_WS, .dout = I2S_GPIO_UNUSED, .din = PIN_I2S_DIN},
  };
  standard_config.slot_cfg.slot_mask = I2S_STD_SLOT_LEFT;
  err = i2s_channel_init_std_mode(rx_channel, &standard_config);
  if (err != ESP_OK) return err;
  i2s_event_callbacks_t callbacks = {.on_recv = on_i2s_receive};
  err = i2s_channel_register_event_callback(rx_channel, &callbacks, NULL);
  if (err != ESP_OK) return err;
  return i2s_channel_enable(rx_channel);
}

esp_err_t vaanicore_audio_read(int16_t *samples, size_t sample_count, size_t *samples_read) {
  if (!rx_channel || !samples || !samples_read) return ESP_ERR_INVALID_ARG;
  size_t bytes_read = 0;
  int32_t *raw = heap_caps_malloc(sample_count * sizeof(int32_t), MALLOC_CAP_INTERNAL);
  if (!raw) return ESP_ERR_NO_MEM;
  esp_err_t err = i2s_channel_read(rx_channel, raw, sample_count * sizeof(int32_t), &bytes_read, 1000);
  size_t count = bytes_read / sizeof(int32_t);
  for (size_t i = 0; i < count; ++i) {
    int32_t shifted = raw[i] >> 14;
    samples[i] = shifted > 32767 ? 32767 : shifted < -32768 ? -32768 : (int16_t)shifted;
  }
  *samples_read = count;
  free(raw);
  return err;
}
