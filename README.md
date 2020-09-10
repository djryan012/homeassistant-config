This is my configuration for Home Assistant.

I'm currently running [Home Assistant](https://home-assistant.io) version __0.114.4__ with the HassOS running on Raspberry Pi 4 with 4gb. Switched back to Hass OS image due to the supervisor not being supproted by my Ubuntu installation.
I still rely on repositories of other HA users for ideas and example code. 

Current status of my Github copy of my Home Assistant is according to travis-ci.com.

<a href="https://travis-ci.com/djryan012/homeassistant-config"><img src="https://travis-ci.com/djryan012/homeassistant-config.svg?branch=master"/></a>

I have been using [Home Assistant](https://home-assistant.io) since July 2017 with version __0.48.0__.


# Ubuntu Server Running Hassio +
Ubuntu server running on an old Dell Inspiron laptop with docker containers. I have installed the Hassio Supervisor Docker version of Home Assistant.

### Docker Container also running
* <a href="https://unifi-network.ui.com/">Unifi Controller</a>
* <a href="* https://www.portainer.io/">Portainer</a>
* <a href= "https://github.com/FalconChristmas/fpp">FPP Christmas</a>
* <a href= "https://containrrr.dev/watchtower">Watchtower</a>

### Hassio Addons
* Mosquitto MQTT Broker 
* Node-Red
* Samba
* TasmoAdmin
* deConz
* <a href="https://github.com/TD22057/insteon-mqtt">Insteon-MQTT</a> (Custom addon)
* Lets Encrypt

# Hassio UI Based Integrations
* Alexa Media Player
* Blue Iris NVR
* deCONZ
* ecoBee
* HACS
* Mobile App
* MQTT
* PLEX
* Roku
* Ubiquiti Unifi
* SolarEdge

# Connected Devices
## Hardwired Devices
* USB Conbee II Gateway
* Insteon  PLM (Switches, Keypad, FanLinc, Micro Dimmers/Switches, Door/Window Sensors, and Motion)  
* Unifi (Gateway, Switch, AP)
* BlueIris on its own Computer (moved away from zoneminder)

## Zigbee Devices
* Ikea TRÅDFRI LED Bulbs
* Ikea TRÅDFRI Motion Sensors
* Philips 

## Wifi Connected Devices
* Sonoff Relays (Basic & POW flashed wtih Tasmota)
* Ecobee 3 (with 3 remote sensors)
* Alexa (Two Echo Dots and One Echo Input)
* <a href="https://github.com/pkozul/ha-floorplan">Floorplan</a> on 10" AlexaFire Wall mounted using <a href="https://github.com/thanksmister/wallpanel-android">Wallpanel</a>

## Phone Apps
* HA Mobile Companion ((tracking, notifications, battery)
* Tasker APP (RestAPI post for sleeping state ~~and charging states~~)
* Telegram for Notifications

## Deprecated
* Zanzito APP (tracking, notifications, alarm clock) Developer not supporting
* Tradfri Lighting Gateway (Have moved to Deconz addon with a Conbee II Gateway due Tradfri gateway drop outs and adding other Zigbee products to house).