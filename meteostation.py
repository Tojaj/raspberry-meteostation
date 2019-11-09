#!/usr/bin/env python

import time

import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont

import Adafruit_DHT
import Adafruit_BMP.BMP085
import Adafruit_SSD1306


# Humidity & Temperature Sensor
HUM_SENSOR = Adafruit_DHT.DHT11  # Sensor type
HUM_PIN = 4  # GPIO pin where humidity sensor data out is conntected

# Barometric Pressure Sensor
BPS_ADDR = 0x77  # I2C address of the sensor
BPS_MODE = 1
# Available modes:
# 0 - Ultra low power
# 1 - Standard
# 2 - High resolution
# 3 - Ultra high resolution


class Disp(object):

    LEFT_PADDING = 0

    def __init__(self, disp):
        """Display object abstraction for text output"""
        self.disp = disp

        # Init display
        disp.begin()
        disp.clear()
        disp.display()

        self.width = disp.width
        self.height = disp.height

        # Prepare image and drawing
        # 1-bit pixels, black and white, stored with one pixel per byte
        self.image = PIL.Image.new('1', (self.width, self.height))
        self.draw = PIL.ImageDraw.Draw(self.image)

        # Load font
        self.font = PIL.ImageFont.load_default()

    def set_contrast(self, contrast):
        """Set display contrast. Value must be between 0 and 255."""
        if contrast < 0 or contrast > 255:
            return False
        self.disp.set_contrast(contrast)
        return True

    def load_truetype_font(self, fn, size=15):
        """Load a TrueType or OpenType font"""
        self.font = PIL.ImageFont.truetype(fn, size)

    def clear(self, display=False):
        """Clear display"""
        self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)
        if display:
            self.disp.image(self.image)
            self.disp.display()

    def display(self, temp, humidity, pressure):
        """Show values on display"""
        self.clear()
        self.draw.text((self.LEFT_PADDING, 0),
                       "Temperature: {:.1f} C   ".format(temp),
                       font=self.font, fill=255)
        self.draw.text((self.LEFT_PADDING, 17),
                       "Humidity: {:.1f} %Rh   ".format(humidity),
                       font=self.font, fill=255)
        self.draw.text((self.LEFT_PADDING, 34),
                       "Pressure: {:.1f} hPa   ".format(pressure),
                       font=self.font, fill=255)
        self.disp.image(self.image)
        self.disp.display()


def loop(bmp, disp):
    """Main loop"""

    while True:

        # Humidity & Temp

        hs_hum, hs_temp = Adafruit_DHT.read_retry(HUM_SENSOR, HUM_PIN)

        # Pressure & Temp

        ps_pressure = bmp.read_pressure()
        ps_temp = bmp.read_temperature()
        ps_alt = bmp.read_altitude()

        # Output to display
        disp.display(ps_temp, hs_hum, ps_pressure / 100.0)

        # Output to console

        if hs_temp is not None:
            print("Temp: {:.1f} C".format(hs_temp))
        else:
            print("Temp is not available")
        if hs_hum is not None:
            print("Humidity: {:.1f} %RH".format(hs_hum))
        else:
            print("Humidity is not available")

        print("Temp: {:.1f} C".format(ps_temp))
        print("Pressure: {:.1f} hPa".format(ps_pressure / 100.0))
        print("Altitude: {:.1f} m".format(ps_alt))
        print("")

        time.sleep(1)


def main():

    # Barometric Pressure Sensor
    bmp = Adafruit_BMP.BMP085.BMP085(mode=BPS_MODE, address=BPS_ADDR)

    # OLED Display
    oled_disp = Adafruit_SSD1306.SSD1306_128_64(rst=None)
    disp = Disp(oled_disp)

    # Custom font
    #disp.load_truetype_font("fonts/Retron2000.ttf", size=10)
    #disp.load_truetype_font("fonts/visitor1.ttf", size=10)
    #disp.load_truetype_font("fonts/PIXELADE.TTF", size=17)

    # Contrast
    disp.set_contrast(255)

    # Main loop
    try:
        loop(bmp, disp)
    except KeyboardInterrupt:
        print("Exiting")
        disp.clear(display=True)
        return


if __name__ == "__main__":
    main()

