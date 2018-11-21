import sys, time, json

# this program will be excecuted from user interface / values [get values button] and print will contain all sensor values

# JSON printing is extra-important, without it user interface cannot read (and present) results

# path to handlers

arduino = '/home/pi/desalinator_sw/ui/handlers/sensors/arduino'
temperature = '/home/pi/desalinator_sw/ui/handlers/sensors/temperature'
mbus = '/home/pi/desalinator_sw/ui/handlers/sensors/mbus/'
relay = '/home/pi/desalinator_sw/ui/handlers/sensors/component_status'


# getting data from arduino
sys.path.append(arduino)
import arduino
arduinoValues = arduino.getValues()

# getting data from 1-wire system
sys.path.append(temperature)
import temperature
temperatureValues = temperature.getValues()

#getting mbusdata from sharky
sys.path.append(mbus)
import mbus
mbusValues = mbus.getValues()

sys.path.append(relay)
import component_status
components = component_status.getValues()



	# inserting data in one object
sensorRes = arduinoValues.copy()
sensorRes.update(temperatureValues)
sensorRes.update(mbusValues)
sensorRes.update(components)



json_raw = json.dumps(sensorRes)


print json_raw


