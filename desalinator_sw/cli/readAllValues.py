import sys


# this program will call handlers and present returned data on command line


# path to handlers

#pressure and levelsensors -> by arduino
arduino = '/home/pi/desalinator_sw/cli/handlers/arduino'

#temperature sensors
temperature = '/home/pi/desalinator_sw/cli/handlers/temperature'

# mbus data from sharky
mbus = '/home/pi/desalinator_sw/cli/handlers/mbus'

# Statuses from relay
relay = '/home/pi/desalinator_sw/cli/handlers/component_status'


print "getting values... "

# getting data from arduino
sys.path.append(arduino)
import arduino

print "pressures and levels ...(1/4)"

#store result in variable
arduinoValues = arduino.getValues()


# getting data from 1-wire system
sys.path.append(temperature)
import temperature

print "temperatures ...(2/4)"
#store result in variable
temperatureValues = temperature.getValues()

#getting mbusdata from sharky
sys.path.append(mbus)
import mbus

print "mbus ...(3/4)"
mbusValues = mbus.getValues()

print "relay ...(4/4)"
sys.path.append(relay)
import component_status

components_status, relay_status = component_status.getValues()



print "pressure and levels"
for i in arduinoValues:
	print i

print "\ntemperatures"	
for i in temperatureValues:
	print i

print "\nmbus data"	
for i in mbusValues:
	print i
	
print "\n relay statuses, False = normal stage"
for i in relay_status:
	print i

print "done"




