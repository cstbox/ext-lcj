# CSTBox extension for LCJ NMEA products support

This repository contains the code for the extension adding the support
for LCJ NMEA based products in the [CSTBox framework](http://cstbox.cstb.fr). 

LCJ products are industrial modules for wind measures. More details can be found
on their [Web site](http://lcjcapteurs.com/).

The support comes in two forms :

  * product drivers generating CSTBox events from produced NMEA sentences
  * products definition files (aka metadata) driving the associated Web configuration editor
    pages

## Currently supported products

  * **CV7C ultrasonic anemometer**
      * outputs : wind speed, direction and temperature

## Runtime dependencies

This extension requires the CSTBox core and serial NMEA support extension to be already installed.
