This is my configuration for Home Assistant.

I'm currently running [Home Assistant](https://home-assistant.io) version __0.105.0__ with the Hassio OS.  (https://home-assistant.io/hassio/). I have moved all files that would use the "!include" syntax to there own folder for better orginization and quicker editing.

Github copy of <a href="https://travis-ci.com/djryan012/homeassistant-config"><img src="https://travis-ci.com/djryan012/homeassistant-config.svg?branch=master"/></a> according to travis-ci.com

# Hardware Running Hassio
* [Raspberry Pi 3](http://a.co/8dDGqmT)

# System integration includes
* Tradfri Lighting
* <a href="https://github.com/TD22057/insteon-mqtt">Insteon-MQTT</a> PLM (Switches, Keypad, FanLinc, Micro Dimmers/Switches, Door/Window Sensors, and Motion)  
* Sonoff Relays (Basic & POW flashed wtih Tasmota)
* Ecobee 3 (with 3 remote sensors)
* Alexa (Two Echo Dots)
* Tasker APP (RestAPI post for sleeping and charging)
* Zanzito APP (tracking, notifications, alarm clock)
* Custom Component Hacs
* BlueIris (moved away from zoneminder)
* <a href="https://github.com/pkozul/ha-floorplan">Floorplan</a> on 10" AlexaFire Wall mounted using <a href="https://github.com/thanksmister/wallpanel-android">Wallpanel</a>
* MQTT
* SolarEdge
* Lets Encrypt
* Unifi Controller
* UPnP

I have been using [Home Assistant](https://home-assistant.io) since July 2017 with version __0.48.0__.
