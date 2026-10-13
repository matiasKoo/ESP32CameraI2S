//parts of his code are taken from
//https://github.com/igrr/esp32-cam-demo
//by Ivan Grokhotkov
//released under Apache License 2.0

#include "XClk.h"
#include "driver/ledc.h"
//oma lisäys, sisältää ilmeisesti vanhentuneet periph_module_enable() ja periph_module_disable
#include "esp_private/periph_ctrl.h"
#include "Log.h"

bool ClockEnable(int pin, int Hz)
{
    periph_module_enable(PERIPH_LEDC_MODULE);

    ledc_timer_config_t timer_conf;
    //alkuperäinen kommentoitu, kirjastot päivittynyt
    //timer_conf.bit_num = (ledc_timer_bit_t)1;
    timer_conf.duty_resolution = (ledc_timer_bit_t)1;
    timer_conf.freq_hz = Hz;
    timer_conf.speed_mode = LEDC_HIGH_SPEED_MODE; //vaihdettu high speed modesta koska lankku valittaa
    timer_conf.timer_num = LEDC_TIMER_0;
    //rivi oma lisäys, LEDC not initialized virheenä, clk kenttä puuttuu timer_conf:sta
    timer_conf.clk_cfg = LEDC_AUTO_CLK;
    timer_conf.deconfigure = false;


    esp_err_t err = ledc_timer_config(&timer_conf);
    if (err != ESP_OK) {
        return false;
    }

    ledc_channel_config_t ch_conf;
    ch_conf.channel = LEDC_CHANNEL_0;
    ch_conf.timer_sel = LEDC_TIMER_0;
    ch_conf.intr_type = LEDC_INTR_DISABLE;
    ch_conf.duty = 1;
    ch_conf.speed_mode = LEDC_HIGH_SPEED_MODE;
    //ch_conf.speed_mode = LEDC_LOW_SPEED_MODE; //vaihdettu high speed modesta koska lankku valittaa
    ch_conf.sleep_mode = LEDC_SLEEP_MODE_NO_ALIVE_NO_PD; //sleep_mode argument invalid, kokeillaan tätä
    ch_conf.gpio_num = pin;
    
    ch_conf.hpoint = 0;//added by me
    
    err = ledc_channel_config(&ch_conf);
    if (err != ESP_OK) {
        return false;
    }
    return true;
}

void ClockDisable()
{
    periph_module_disable(PERIPH_LEDC_MODULE);
}

