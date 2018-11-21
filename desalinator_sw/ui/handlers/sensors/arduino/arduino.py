import serial, time


# This handler is almost same as commandline side arduino handler
# except the return value type is dictionary object


address = '/dev/arduino'
baudrate = 19200
timeout = 1



def calcPressure(Vout):
	Vs = 5.1
	CorrectionFactor = 1.013/0.978
	pressure = float(((Vout/Vs+0.04)/0.004)/100*CorrectionFactor)
	pressure = round(pressure, 2)
	return pressure

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

	# BOTTON LEVEL SENSOR OF INTAKE TANK
	serialCom.write("0xD1")
	value5 = serialCom.readline()
	if float(value5) < 1:
		bottomLevel = False
	else:
		bottomLevel = True
			
	serialCom.close()
	
	returnValue = {
	'arduino_inner_top_pressure':pressure_inner_top,
	'arduino_outer_top_pressure':pressure_outer_top,
	'arduino_bottom_pressure':pressure_bottom,
	'arduino_top_level_sensor':topLevel,
	'arduino_bottom_level_sensor':bottomLevel
	}
	
	return returnValue