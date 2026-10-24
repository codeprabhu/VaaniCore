#pragma once
#include "freertos/FreeRTOS.h"
#include "freertos/queue.h"
#include "esp_err.h"
#include <stdbool.h>

typedef enum { VC_UI_PTT, VC_UI_CONFIRM, VC_UI_ABORT, VC_UI_MUTE } vc_ui_event_t;
esp_err_t vaanicore_ui_init(QueueHandle_t event_queue);
void vaanicore_ui_leds(bool listening, bool busy, bool error);
