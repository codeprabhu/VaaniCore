#pragma once
#include "context.h"

/* Requires nvs_flash_init() during firmware startup. */
int vc_history_load_nvs(vc_history_t *history);
int vc_history_save_nvs(const vc_history_t *history);
