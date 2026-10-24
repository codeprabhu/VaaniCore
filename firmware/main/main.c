/* ESP-IDF integration skeleton: hardware execution is not claimed in bootstrap. */
#include "pins.h"
void app_main(void) {
  /* Planned: I2S GDMA callback -> task notification; no work is done in ISR. */
  (void)PIN_I2S_BCLK;
}
