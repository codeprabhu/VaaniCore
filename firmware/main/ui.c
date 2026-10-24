#include "ui.h"
#include "driver/gpio.h"
#include "pins.h"
#include <stdint.h>

static QueueHandle_t events;

static void IRAM_ATTR button_isr(void *arg) {
  vc_ui_event_t event = (vc_ui_event_t)(uintptr_t)arg;
  BaseType_t higher_priority_task_woken = pdFALSE;
  xQueueSendFromISR(events, &event, &higher_priority_task_woken);
  if (higher_priority_task_woken) portYIELD_FROM_ISR();
}

esp_err_t vaanicore_ui_init(QueueHandle_t event_queue) {
  if (!event_queue) return ESP_ERR_INVALID_ARG;
  events = event_queue;
  gpio_config_t buttons = {.pin_bit_mask = (1ULL << PIN_BUTTON_CONFIRM) | (1ULL << PIN_BUTTON_ABORT) | (1ULL << PIN_MUTE_SENSE), .mode = GPIO_MODE_INPUT, .pull_up_en = GPIO_PULLUP_ENABLE, .pull_down_en = GPIO_PULLDOWN_DISABLE, .intr_type = GPIO_INTR_NEGEDGE};
  esp_err_t err = gpio_config(&buttons);
  if (err != ESP_OK) return err;
  gpio_config_t leds = {.pin_bit_mask = (1ULL << PIN_LED_LISTEN) | (1ULL << PIN_LED_BUSY) | (1ULL << PIN_LED_ERR), .mode = GPIO_MODE_OUTPUT, .pull_up_en = GPIO_PULLUP_DISABLE, .pull_down_en = GPIO_PULLDOWN_DISABLE, .intr_type = GPIO_INTR_DISABLE};
  err = gpio_config(&leds);
  if (err != ESP_OK) return err;
  gpio_install_isr_service(0);
  gpio_isr_handler_add(PIN_BUTTON_CONFIRM, button_isr, (void *)(uintptr_t)VC_UI_CONFIRM);
  gpio_isr_handler_add(PIN_BUTTON_ABORT, button_isr, (void *)(uintptr_t)VC_UI_ABORT);
  gpio_isr_handler_add(PIN_MUTE_SENSE, button_isr, (void *)(uintptr_t)VC_UI_MUTE);
  return ESP_OK;
}

void vaanicore_ui_leds(bool listening, bool busy, bool error) {
  gpio_set_level(PIN_LED_LISTEN, listening); gpio_set_level(PIN_LED_BUSY, busy); gpio_set_level(PIN_LED_ERR, error);
}
