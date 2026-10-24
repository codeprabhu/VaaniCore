#pragma once
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_err.h"
#include <stddef.h>
#include <stdint.h>

esp_err_t vaanicore_audio_init(TaskHandle_t notify_task);
esp_err_t vaanicore_audio_read(int16_t *samples, size_t sample_count, size_t *samples_read);
