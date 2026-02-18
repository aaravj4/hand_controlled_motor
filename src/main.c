#include "driver/ledc.h"
#include "driver/uart.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

#define MOSFET_PIN 25
#define PWM_CHANNEL 0
#define PWM_FREQ 5000
#define PWM_RES LEDC_TIMER_8_BIT
#define UART_PORT UART_NUM_0

void app_main(void)
{
    uart_driver_install(UART_PORT, 256, 0, 0, NULL, 0);

    ledc_timer_config_t ledc_timer = {
        .speed_mode = LEDC_HIGH_SPEED_MODE,
        .timer_num = LEDC_TIMER_0,
        .duty_resolution = PWM_RES,
        .freq_hz = PWM_FREQ,
        .clk_cfg = LEDC_AUTO_CLK
    };
    ledc_timer_config(&ledc_timer);

    ledc_channel_config_t ledc_channel = {
        .speed_mode = LEDC_HIGH_SPEED_MODE,
        .channel = PWM_CHANNEL,
        .timer_sel = LEDC_TIMER_0,
        .intr_type = LEDC_INTR_DISABLE,
        .gpio_num = MOSFET_PIN,
        .duty = 0,
        .hpoint = 0
    };
    ledc_channel_config(&ledc_channel);

    ledc_set_duty(LEDC_HIGH_SPEED_MODE, PWM_CHANNEL, 0);
    ledc_update_duty(LEDC_HIGH_SPEED_MODE, PWM_CHANNEL);

    uint8_t data;
    while (1) {
        int len = uart_read_bytes(UART_PORT, &data, 1, 10);
        if (len > 0) {
            if (data == '1') {
                ledc_set_duty(LEDC_HIGH_SPEED_MODE, PWM_CHANNEL, 255);
                ledc_update_duty(LEDC_HIGH_SPEED_MODE, PWM_CHANNEL);
            } else if (data == '0') {
                ledc_set_duty(LEDC_HIGH_SPEED_MODE, PWM_CHANNEL, 0);
                ledc_update_duty(LEDC_HIGH_SPEED_MODE, PWM_CHANNEL);
            }
        }
        vTaskDelay(1);
    }
}
