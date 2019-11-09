Raspberry Meteostation
======================

A simple Raspberry Pi based meteostation with DHT11 & BMP180 sensors
and OLED display SSD1306.

Usage
=====

    $ ./meteostation.py

The OLED will start showing temperature, humidity and barometric pressure.
Output on console will be like:

    Temp: 24.0 C
    Humidity: 60.0 %RH
    Temp: 24.7 C
    Pressure: 980.2 hPa
    Altitude: 279.3 m

    ...

* First temperature is from DHT11 sensor, the second from BMP180.
* OLED shows the temperature from BMP180.


Requirements
============

**Hardware components**

* DHT11 - Humidity & Temperature Sensor
* BMP180 - Barometric Pressure Sensor
* OLED display 128x64 I2C (SSD1306)
* Raspberry Pi with Raspbian (I have used Raspberry Pi Zero)
* 1x 10K resistor (as a pull-up for DHT11 between VCC and DATA)
* Few wires

**Raspbian packages**

    sudo apt-get install -y \
        build-essential \
        python-dev \
        python-openssl \
        python-pil \
        python-smbus \
        i2c-tools

**PIP libraries**

*Note: Before you install python modules by pip, you should consider
use of a python virtual environments. See next section of this readme.*

    pip install -r requirements.txt


Installation in virtual env
===========================

**1)** Install all necessary packages:

    sudo apt-get install virtualenv virtualenvwrapper

**2)** Add the next two lines at the bottom of your ``~/.profile`` file:

    export WORKON_HOME=~/.virtualenvs
    source /usr/share/virtualenvwrapper/virtualenvwrapper.sh

Note: If you have ~/.bash_profile file, then you need to add it there
as in that case the ``~/.profile`` won't be read.

**3)** Create a virtual env

    mkvirtualenv --system-site-packages raspberry-meteostation

Note: We are allowing system site python packages to be available in our
virtual env here.

**When you are ready to work** on the new virtual env

    workon raspberry-meteostation

**Once you are done** deactivate the virtual env

    deactivate


Troubleshooting
===============

List devices available on I2C bus and their addresses:

    i2cdetect -y 1
