import os

# This handler is almost same as commandline temperature handler
	# Return value type is dictionary object

def getAdressesAndPositions():

	# get addresses of sensors
	file = open("/home/pi/desalinator_sw/lib/sensorInfo/sensor_conf.txt", "r")
	addresses = file.readlines()
	addresses = map(str.strip, addresses)
	
	# get physical positions of sensors
	file2 = open("/home/pi/desalinator_sw/lib/sensorInfo/sensor_positions.txt", "r")
	positions = file2.readlines()
	positions = map(str.strip, positions)
	
	
	file.close()
	file2.close()
	return addresses, positions
	
	
def getValues():

	retVal = []
	retErr = []

	# calling adresses and positions
	address, position = getAdressesAndPositions()
	
	# First start owfs system
	os.system('sudo bash /etc/init.d/owfs start > /dev/null')
	
	ii = 0
	
	for i in address:
		try:
			tempFile=os.path.join("/","mnt","1wire",i,"temperature")
			tempByAddress=open(tempFile,'r')  
			degree=tempByAddress.read()
			temp = (degree)
			retVal.append(temp)
			tempByAddress.close()
			ii += 1

		except Exception as e:
			os.system('sudo bash /etc/init.d/owfs start > /dev/null')
			retErr.append(i)
			
	if len(address) != len(retVal):
		for i in retErr:
			if len(i) > 5:
				retVal.append("System cant read some temperature information from address:  " + i)
				
	
	retData = {
	'temperature_dimense_27' : float(retVal[0]),
	'temperature_dimense_77' : float(retVal[1]),
	'temperature_dimense_127' : float(retVal[2]),
	'temperature_dimense_177' : float(retVal[3]),
	'temperature_dimense_227' : float(retVal[4]),
	'temperature_dimense_277' : float(retVal[5]),
	'temperature_dimense_327' : float(retVal[6]),
	'temperature_dimense_377' : float(retVal[7]),
	'temperature_dimense_427' : float(retVal[8]),
	'temperature_individual_salt_drain' : float(retVal[9]),
	'temperature_individual_dw' : float(retVal[10]),
	'temperature_individual_sw_input' : (retVal[11]),
	
	}
			
	return retData
	
	
	