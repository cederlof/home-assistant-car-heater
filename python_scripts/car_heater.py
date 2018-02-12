#variables to modify in script
heater_switch_id = "switch.z2_switch_switch"
temperature_sensor_id = "sensor.27_temperature"

#get or create enable-state for automation
heater_enable_boolean = "input_boolean.enable_heater_automation";
#logger.warning("CAR_HEATER {}".format(1))
#if enabled
if hass.states.get(heater_enable_boolean).state is 'on':
#	logger.warning("CAR_HEATER {}".format(2))
	now = datetime.datetime.now()

	#variables to set from gui
	departure_time_input = hass.states.get("input_datetime.heater_departure_time_input")
	departure_time_hours = int(departure_time_input.attributes["hour"])
	departure_time_minutes = int(departure_time_input.attributes["minute"])

	#we're assuming lift off is during todays date, will be problematic around midnight..
	departure_time = datetime.datetime(now.year, now.month, now.day, departure_time_hours, departure_time_minutes, 0)
	if departure_time < now:
		departure_time = departure_time + datetime.timedelta(days = 1)

#	logger.warning("CAR_HEATER {}".format(3))
	hass.states.set('sensor.heater_departure_time', departure_time, {
		'friendly_name': 'Avresetid',
		'icon': 'car,'
	})

	#stop using the heater above this temperature
	max_temperature = 10

	#fetch the temperature from the sensor
	temperature = hass.states.get(temperature_sensor_id).state

#	logger.warning("CAR_HEATER {} temp {} isfloat {}".format(4, temperature, temperature.lstrip('-').replace('.','',1).isdigit()))
	#check that we are below the max temp for using the heater
	if temperature.lstrip('-').replace('.','',1).isdigit() and float(temperature) <= float(max_temperature):
#		logger.warning("CAR_HEATER {}".format(5))
		heater_switch_status_states = hass.states.get(heater_switch_id)
		heater_switch_status = heater_switch_status_states.state

#		logger.warning("CAR_HEATER {}".format(6))
		#how early should we start the heater
		temperature_float = float(temperature)
		if temperature_float <= -10:
			delta = datetime.timedelta(hours = 2)
		elif temperature_float <= 0:
			delta = datetime.timedelta(hours = 1)
		elif temperature_float <= max_temperature:
			delta = datetime.timedelta(minutes = 30)
		start_heater_time = departure_time - delta

		heater_should_be_on = start_heater_time < now and departure_time > now

#		logger.warning("CAR_HEATER {}".format(7))
		#toggle the heater switch
		if heater_switch_status is 'off' and heater_should_be_on:
			hass.services.call('switch', 'turn_on', {'entity_id': heater_switch_id})
			hass.services.call('notify','telegram', {"message": "Motorvärmaren startas."})
		if heater_switch_status is 'on' and not heater_should_be_on:
			hass.services.call('switch', 'turn_off', {'entity_id': heater_switch_id})
			hass.services.call('notify','telegram', {"message": "Motorvärmaren stängs av."})

#		logger.warning("CAR_HEATER {}".format(8))
		hass.states.set('sensor.heater_will_run_when', start_heater_time, {
			'friendly_name': 'Motorvärmare startas',
			'icon': 'mdi:av-timer',
		})
		#logger.warning("sensor heater_will_run_when {}".format(start_heater_time))
#	else:
#		logger.warning("CAR_HEATER {}".format(9))