This fork serves as a platform for testing an OV7670 module for further development purposes

Versions used:
Arduino IDE 2.3.10
esp32 (by Espressif Systems) 3.3.11
Adafruit GFX Library 1.12.6
Adafruit ST7735 and ST7789 Library 1.11.0

# ESP32 I2S Camera

This project shows how to record images with the ESP32 and the OV7670 camera without FIFO. An SPI TFT display is supported and a basic web server provides the images in the local network.

The video explaining this code can be found here
https://youtu.be/S2yTQHM82jc

Also check out the project page for some details, parts and datasheets
http://bitluni.net/esp32-i2s-camera-ov7670/

# Acknowledgements
The project is based on the esp-cam-demo by Ivan Grokhotkov
https://github.com/igrr/esp32-cam-demo

#License
Since parts of the code are taken from the esp-cam-demo which are subject to the Apache License 2.0 license. You will find a note in at the top of the respective files.
The rest of the code is Public Domain

#The code is based on the ESP32 integration in the Arduino IDE. You need:

Arduino IDE

ESP32 integration

Adafruit GFX library

Adafruit ST7735 library

