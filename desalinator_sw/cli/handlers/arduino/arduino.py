import serial, time



	#serial communication parameters
address = '/dev/arduino'
baudrate = 19200
timeout = 1

# serial messages to Arduino
	# Top pressure sensor, placed inner pipe is connected to arduino port "A0"
	# Top pressure sensor, placed outer pipe is connected to arduino port "A1"
	# Bottom pressure sensor, placed bottom of pipe is connected to arduino port "A2"
	# Top level sensor, placed seawater intake tank physically higher stage is connected to arduino pin "2"
	# Low level sensor, placed seawater intake tank physically lower stage is connected to arduino pin "3"
		# sending message type is string, see content of message from getValue or getValues functions
		# Arduino will answer message with voltage value (Level sensors will be high as 1.00 or low as 0.00)
			# 1.00 means true for water and vice-versa


	# will return calculated pressure value from voltage value	
		# formula is from pressuresensors datasheet
		# CorrectionFactor is evolved with calculated value (without correction) divided with current pressure value (foreca/kokkola)
		# this function is called from each pressuresensor values
def calcPressure(Vout):
	Vs = 5.1
	CorrectionFactor = 1.013/0.978
	pressure = float(((Vout/Vs+0.04)/0.004)/100*CorrectionFactor)
	pressure = round(pressure, 2)
	return pressure

	
	# this function is not in use in system
		# will return individual value of parameter sensor identity
		# level sensorvalues will be returned by boolean variable
		# Pressuresensor variables will be returned by float which rounded on 2 dec
def getValue(sensor):
	if sensor == "innertop":
		serialCom = serial.Serial(address, baudrate=baudrate, timeout=timeout)
		time.sleep(2)
		serialCom.write("0xA0")
		value1 = serialCom.readline()
		pressure1 = calcPressure(float(value1))
		return pressure1

	
	if sensor == "outertop":
		serialCom = serial.Serial(address, baudrate=baudrate, timeout=timeout)
		time.sleep(2)
		serialCom.write("0xA1")
		value2 = serialCom.readline()
		pressure2 = calcPressure(float(value2))
		return pressure2
	
	if sensor == "bottom":
		serialCom = serial.Serial(address, baudrate=baudrate, timeout=timeout)
		time.sleep(2)
		serialCom.write("0xA2")
		value3 = serialCom.readline()
		pressure3 = calcPressure(float(value3))
		return pressure3
		

		
	if sensor == "toplevel":
		serialCom = serial.Serial(address, baudrate=baudrate, timeout=timeout)
		time.sleep(2)
		serialCom.write("0xD0")
		value4 = serialCom.readline()
		if float(value4) < 1:
			return False
		else:
			return True

	if sensor == "bottomlevel":
		serialCom = serial.Serial(address, baudrate=baudrate, timeout=timeout)
		time.sleep(2)
		serialCom.write("0xD1")
		value5 = serialCom.readline()
		if float(value5) < 1:
			return False
		else:
			return True
			
	serialCom.close()
	
	

	# This function is in use on readAllvalues.py program
		# this function will call local calcPressure -function
		# all produced values will be returned on list object which contain location information on same index
def getValues():

	# connection
	serialCom = serial.Serial(address, baudrate=baudrate, timeout=timeout)
	time.sleep(2)
		
		
	# INNER TOP PRESSURE SENSOR
	serialCom.write("0xA0")
	value1 = serialCom.readline()
	pressure_inner_top = calcPressure(float(value1))

	# OUTER TOP PRESSURE SENSOR
	serialCom.write("0xA1")
	value2 = serialCom.readline()
	pressure_outer_top = calcPressure(float(value2))
	
	
	# BOTTOM PRESSURE SENSOR
	serialCom.write("0xA2")
	value3 = serialCom.readline()
	pressure_bottom = calcPressure(float(value3))

		

	# TOP LEVEL SENSOR OF INTAKE TANK
	serialCom.write("0xD0")
	value4 = serialCom.readline()
	if float(value4) < 1:
		topLevel = False
	else:
		topLevel = True

	# BOTTOM LEVEL SENSOR OF INTAKE TANK
	serialCom.write("0xD1")
	value5 = serialCom.readline()
	if float(value5) < 1:
		bottomLevel = False
	else:
		bottomLevel = True
			
	serialCom.close()
	
	returnValue = [
	'inner top pressure:  ' +str(pressure_inner_top),
	'outer top pressure:  ' + str(pressure_outer_top),
	'bottom pressure:     ' + str(pressure_bottom),
	'top level sensor:    ' + str(topLevel),
	'bottom level sensor: ' + str(bottomLevel)
	]
	
	return returnValue