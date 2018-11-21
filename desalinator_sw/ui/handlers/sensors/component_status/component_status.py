import serial, time


# this handler will be most same than commandline component status handler
# Except here will be component statusses presented on strings
	# Return value type is dictionary object


def getFromRelay():
	serialCom = serial.Serial('/dev/relay',9600, timeout=3)
	request = chr(0xFF) + chr (0xA1) + chr (0x00)
	serialCom.write(request)
	time.sleep(1)
	raw_result = str(serialCom.readlines())
	serialCom.close()
	return raw_result
	

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
	
		# individual component stages
	if component[0]:
		component[0] = "open"
	else:
		component[0] = "closed"
		
	if component[1]:
		component[1] = "open"
	else:
		component[1] = "closed"
		
	if component[2]:
		component[2] = "closed"
	else:
		component[2] = "open"
		
	if component[3]:
		component[3] = "open"
	else:
		component[3] = "closed"
		
	if component[4]:
		component[4] = "on"
	else:
		component[4] = "off"
		
	if component[5]:
		component[5] = "on"
	else:
		component[5] = "off"
		
	if component[6]:
		component[6] = "controlled stage"
	else:
		component[6] = "normal stage"
		
	if component[7]:
		component[7] = "controlled stage"
	else:
		component[7] = "normal stage"
		
	'''	
	retRelay = {
	'R1': relay[0],
	'R2': relay[1],
	'R3': relay[2],
	'R4': relay[3],
	'R5': relay[4],
	'R6': relay[5],
	'R7': relay[6],
	'R8': relay[7]
	}
	'''
	
	
	retComponent = {
	'relay_sw_intake_valve': component[0],
	'relay_sw_out_lwr_valve': component[1],
	'relay_sw_out_upr_valve': component[2],
	'relay_intake_pressure_valve': component[3],
	'relay_vacuum_pump': component[4],
	'relay_circulation_pump': component[5],
	'relay_R7': component[6],
	'relay_R8': component[7]
	}
	
		
	return retComponent
		
		
	
	
