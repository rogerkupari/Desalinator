import sys, json, time, serial
import mysql.connector as my


# this program will be more complex than others in time of writing.
	# this program will be executed by cron routine between the set interval (more information, see mgnCron.py)
		# The execution ends when user will end the test session (more information, see mgnCron.py)
		
	# functions of this program will be commented individually


#Database variables
dbHost = '****'
dbDes = '****'
dbDes2 = '****'
dbUser = '****'
dbPasswd = '****'


	# this function will call all sensor values and return it with dictionary object
def getSensorValues():
		#paths to sensor reading handlers
	arduino = '/home/pi/desalinator_sw/ui/handlers/sensors/arduino'
	temperature = '/home/pi/desalinator_sw/ui/handlers/sensors/temperature'
	mbus = '/home/pi/desalinator_sw/ui/handlers/sensors/mbus'
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



		# inserting data in one dictionary
	sensorRes = arduinoValues.copy()
	sensorRes.update(temperatureValues)
	sensorRes.update(mbusValues)
	sensorRes.update(components)

	return sensorRes
	
	
	# this function read the latest database tablename and will return it type of string
def getLatestTableName():
	ltable = open("/home/pi/desalinator_sw/lib/database_process/temporary/latestTable.txt", "r")
	tableName_raw = ltable.readlines()
	retVal = ""
	for c in tableName_raw:
		retVal += c
	ltable.close()
	
	return retVal
	
	
	# This function will read defined attribute [desalination_test_attr] -database and test result [desalination] -database
		# it will return the values in list object
def databaseColumns():
	attributes_columns_path = '/home/pi/desalinator_sw/lib/database_process/configurations/attribute_columns.txt'
	storage_columns_path = '/home/pi/desalinator_sw/lib/database_process/configurations/storage_columns.txt'
	attributes = open(attributes_columns_path)
	attr_raw = attributes.readlines()
	attr = map(str.strip, attr_raw)
	
	storage = open(storage_columns_path)
	storage_raw = storage.readlines()
	stor = map(str.strip, storage_raw)
	
	attributes.close()
	storage.close()

	return attr, stor
	
	
		# This function calls to get sensor values, latest table name and defined column names
			# Sensor values is gonna stored on test results [desalination] -database
				# if storing process is executed successful function will return boolean true
					# else its returning false
def storeValuesOnDatabase():
	sensors = getSensorValues()
	tableName = getLatestTableName() + " ( "
	xxx, storage_raw = databaseColumns()
	storage = []
	for i in range(0, len(storage_raw)):
		if i == len(storage_raw)-1:
			storage.append(storage_raw[i])
		else:
			storage.append(storage_raw[i] + ", ")
		
	
	try:
		
		db = my.connect(host=dbHost, user=dbUser, password=dbPasswd, database=dbDes)
		c = db.cursor(buffered = True)

		cmd = ("INSERT INTO " + tableName + 
		
		storage[0]+
		storage[1]+
		storage[2]+
		storage[3]+
		storage[4]+
		storage[5]+
		storage[6]+
		storage[7]+
		storage[8]+
		storage[9]+
		
		storage[10]+
		storage[11]+
		storage[12]+
		storage[13]+
		storage[14]+
		storage[15]+
		storage[16]+
		storage[17]+
		storage[18]+
		storage[19]+
		
		storage[20]+
		storage[21]+
		storage[22]+
		storage[23]+
		storage[24]+
		storage[25]+
		storage[26]+
		storage[27]+
		storage[28]+
		storage[29]+
		
		storage[30]+
		storage[31]
		+
		"""
		) 
		VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
		%f, %f, %f, %f, %f, %f, %f, 
		%s, %s,
		%f, %f, %f, 
		'%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"""
		%(
		sensors['temperature_dimense_27'],
		sensors['temperature_dimense_77'],
		sensors['temperature_dimense_127'],
		sensors['temperature_dimense_177'],
		sensors['temperature_dimense_227'],
		sensors['temperature_dimense_277'],
		sensors['temperature_dimense_327'],
		sensors['temperature_dimense_377'],
		sensors['temperature_dimense_427'],
		sensors['temperature_individual_salt_drain'],
		sensors['temperature_individual_dw'],
		sensors['temperature_individual_sw_input'],
		sensors['mbus_total_energy_kwh'],
		sensors['mbus_total_Volume_m3'],
		sensors['mbus_volume_flow_liters'],
		sensors['mbus_power_kw'],
		sensors['mbus_flow_temp_c'],
		sensors['mbus_return_temp_c'],
		sensors['mbus_current_energy_kwh'],
		sensors['arduino_top_level_sensor'],
		sensors['arduino_bottom_level_sensor'],
		sensors['arduino_outer_top_pressure'],
		sensors['arduino_inner_top_pressure'],
		sensors['arduino_bottom_pressure'],
		sensors['relay_sw_intake_valve'],
		sensors['relay_sw_out_lwr_valve'],
		sensors['relay_sw_out_upr_valve'],
		sensors['relay_intake_pressure_valve'],
		sensors['relay_vacuum_pump'],
		sensors['relay_circulation_pump'],
		sensors['relay_R7'],
		sensors['relay_R8'],
		));
		
		c.execute(cmd)
		

		db.commit()
		c.close()
		db.close()
		
		return True

	except Exception as e:
		sys.stderr.write(str(e))
		return False
		
		
		# This function will read the database values and return the values in dictionary object
def readDatabaseValues():
	xxx, storage_raw= databaseColumns()
	storage = []
	outputStorage = []
	storage.append('id, ')
	outputStorage.append('id')
	
	for i in range(0, len(storage_raw)):
		outputStorage.append(storage_raw[i])
		if i == len(storage_raw)-1:
			storage.append(storage_raw[i])
			
		else:
			storage.append(storage_raw[i] + ", ")
		
	
	
	
	tableName = getLatestTableName()
	
	try:
		
		db = my.connect(host=dbHost, user=dbUser, password=dbPasswd, database=dbDes)
		c = db.cursor(buffered = True)

		cmd = ("SELECT " +
		storage[0]+
		storage[1]+
		storage[2]+
		storage[3]+
		storage[4]+
		storage[5]+
		storage[6]+
		storage[7]+
		storage[8]+
		storage[9]+
		storage[10]+
		storage[11]+
		storage[12]+
		storage[13]+
		storage[14]+
		storage[15]+
		storage[16]+
		storage[17]+
		storage[18]+
		storage[19]+
		storage[20]+
		storage[21]+
		storage[22]+
		storage[23]+
		storage[24]+
		storage[25]+
		storage[26]+
		storage[27]+
		storage[28]+
		storage[29]+
		storage[30]+
		storage[31]+
		storage[32]
		+ " FROM " + tableName + " WHERE id =(SELECT max(id) from " +tableName + ");")
		c.execute(cmd)
		result_raw = c.fetchall()[0]
		
		c.close()
		db.close()
		
			
		
	

		bothValues = dict(zip(outputStorage, result_raw))
		
		return bothValues
		
		
	
	except Exception as e:
		sys.stderr.write(str(e))
		
		
		# this function will return the attributes values from database from individual table
def returnAttributes():
	attributes_raw, xxx = databaseColumns()
	
	attributes = []
	outputAttributes = []
	attributes.append('id, ')
	outputAttributes.append('id')
	
	for i in range(0, len(attributes_raw)):
		outputAttributes.append(attributes_raw[i])
		if i == len(attributes_raw)-1:
			attributes.append(attributes_raw[i])
			
		else:
			attributes.append(attributes_raw[i] + ", ")
		
	
	
	
	tableName = getLatestTableName()
	
	try:
		
		db = my.connect(host=dbHost, user=dbUser, password=dbPasswd, database=dbDes2)
		c = db.cursor(buffered = True)

		cmd = ("SELECT " +
		attributes[0]+
		attributes[1]+
		attributes[2]+
		attributes[3]

		+ " FROM " + tableName + " WHERE id =(SELECT max(id) from " +tableName + ");")
		c.execute(cmd)
		result_raw = c.fetchall()[0]
		
		c.close()
		db.close()

		bothValues = dict(zip(outputAttributes, result_raw))
		del bothValues['id']
		
		return bothValues
		
		
	except Exception as e:
		sys.stderr.write(str(e))
		
	
		# this function will look specific pressure sensor value and managet control for vacuum pump by limit values which been placed in UI
def setVacuum(values):


	stat1 = values.copy()
	hi = stat1['vacuum_hi']
	lo = stat1['vacuum_lo']
	value = stat1['pressure_outer_top']

	
		# Serial communication to relay
	serialCom = serial.Serial('/dev/relay',9600, timeout=3)
	vacuum1 = chr(0xFF) + chr (0x05) + chr (0x01)
	vacuum0 = chr(0xFF) + chr (0x05) + chr (0x00)

	if (value >= hi):
		serialCom.write(vacuum1)
		time.sleep(1)
		serialCom.close()

		
	if value <= lo:
		serialCom.write(vacuum0)
		time.sleep(1)
		serialCom.close()

		
	if value > hi and value > lo:
		returnValue = {"vacuum_command": "on"}
	
	if value < hi and value < lo:
		returnValue = {"vacuum_command": "off"}

	
	return returnValue
	

	
	
	
	
	# Function uses
if storeValuesOnDatabase():
	valuesInDatabase = readDatabaseValues()
	attributesInDatabase = returnAttributes()
	
	valuesToUi = valuesInDatabase.copy()
	valuesToUi.update(attributesInDatabase)
	stateOfVacuum = setVacuum(valuesToUi)
	valuesToUi.update(stateOfVacuum)
	print json.dumps(valuesToUi)

else:
	err = {"error": "error occured on testingProgram.py"}
	print err

	
	
	
	#print(readDatabaseValues())

	


