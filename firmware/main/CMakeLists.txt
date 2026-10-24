idf_component_register(SRCS "main.c" "audio_capture.c" "ui.c" INCLUDE_DIRS "." REQUIRES esp_driver_i2s esp_driver_gpio nvs_flash)
