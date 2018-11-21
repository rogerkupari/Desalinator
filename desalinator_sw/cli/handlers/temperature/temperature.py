import os


	#this function will get sensor addresses (usually begin with 28.)
		# and their physical called positions
		# connection between these two textfiles will occured by line index	
			# eg. The first address line will linked to first position
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
	
	
	# This function will call function above
	# This function will be called from readAllValues.py
	# Function will first start the owfs virtual filesystem
		# Then its looking data by readed sensor address
			# if data will not be visible in filesystem, it will start filesystem again
			# if some data is missing, list index will be replaced with error
		# Function will return all readed data (and errors if occured) on list object.
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
			temp = (position[ii] + " : " + i + ": " + degree + " 'C")
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
			
	return retVal
	
	
	