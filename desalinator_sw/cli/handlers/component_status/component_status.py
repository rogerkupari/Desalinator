import serial, time


# handler will call KMtronic with specific request message. In this case "0xA1" mean relay dip position "1".
	# future dip positions will be as "0xA2" wich mean dip position "2", etc..
# KMtronic will answer all 8ch statuses in one message as "0xFF/0xA1/0x00/0x00/0x00 ..."
	#first value after "0xA1" which is "0x00" means in this case the first relay is normal position
		#If value will be "0x01" it means realay is controlled. Relay will return eight values.


	# serial connection function
		# this function will catch the return message and return it
def getFromRelay():
	serialCom = serial.Serial('/dev/relay',9600, timeout=3)
	request = chr(0xFF) + chr (0xA1) + chr (0x00)
	serialCom.write(request)
	time.sleep(1)
	raw_result = str(serialCom.readlines())
	serialCom.close()
	return raw_result

	
	#this function is called from readAllValues.py program
		# this function will call the above connection function
		# Received message will be handled in this function. Names and values will be included own list objects with same index values.
			# see the relay component wiring from electrical documentation
			# Seawater top output value will be inverted in this function
		
def getValues():
	relay = []
	component = []
	fullStatus = getFromRelay()
	
	
		# Status of relay
	for i in range(10, len(fullStatus)):
		if fullStatus[i] == 'x':
			if fullStatus[i+2] == '1':
				relay.append(True)
			else:
				relay.append(False)
			
			
			
		# Status of components
	for i in range(10, len(fullStatus)):
		if fullStatus[i] == 'x':
			if fullStatus[i+2] == '1':
				component.append(True)
			else:
				component.append(False)
	
		# upper sw-out valve is normally opened physically
	if component[2]:
		component[2] = False
	else:
		component[2] = True
		
	return component, relay
		
		
	
	
