# Home Assistant Car Heater

Set your departure time the night before you're leaving the house, and the heater will be run 1 or 2 hours before departure, depending on the outside temperature.

With inspiration from https://github.com/Gnaget2/Car-Heater-Package which uses yaml for everything, which I found painful. The heater logic is instead performed by a python script `python_scripts/car_heater.py`.

I haven't had the time to make this into a proper HASS-package, but hopefully it can be used as inspiration.

Notes:
* `switch.z2_switch_switch` is the name of my switch controlling the heater (from the wall-outlet)
* `sensor.27_temperature` is the name of the thermometer measuring outside temperature
* At the moment:
   * Less than -10 Celcius heater will start 2 hours before departure
   * Less than 0 Celcius heater will start 1 hour before departure
   * Less than +10 Celcius heater will start 30 minutes before departure
* I use Telegram for notifications

---

<img src="images/screenshot.png?raw=true" align="left" width="300px" >