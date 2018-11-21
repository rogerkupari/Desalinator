import subprocess


# This handler will be almost same than commandline mbus handler
	# except return value type is dictionary object


# catch the mbus output from sharky
def getTheData():

	request = subprocess.Popen(["/bin/bash", "-i", "-c", "mbusReq"], stdout=subprocess.PIPE, shell=False)
	data, error = request.communicate()
	data = data.split()
	
	return data, error

values = []


valueNamesAndUnits = [
'Total Energy (kWh)',
'Total Volume (m^3)',
'VolumeFlow (liters)',
'Power (kW): ',
'Flow temperature (Celcius)',
'Return temperature (Celcius)',
'Current Energy (kWh)'
]



def getValues():
	data, error = getTheData()
	if data:
		for id in range(0,7):
			searchSegment1 = "id="+'"'+str(id)+'"'+">"
			searchBetween1 = "<Value>"

			segment1 = data.index(searchSegment1)

			for i in data[segment1:]:
				if searchBetween1 in i:
					RawValue = i
					break

			numberValue = ''.join(number for number in RawValue if number.isdigit())
			values.append(float(numberValue))
			
			if id == 1 or id == 3:
				values[id] = values[id]/1000 #id 1 = m^3 and 3 = kW
				
			elif id == 4 or id == 5:
				values[id] = values[id]/10 # id 4 and 5 = celcius
				

		retData = {
		'mbus_total_energy_kwh': values[0],
		'mbus_total_Volume_m3': values[1],
		'mbus_volume_flow_liters': values[2],
		'mbus_power_kw': values[3],
		'mbus_flow_temp_c': values[4],
		'mbus_return_temp_c': values[5],
		'mbus_current_energy_kwh': values[6]
		}
			
		return retData
		
	else:
		return error