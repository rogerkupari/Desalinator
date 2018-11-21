import subprocess

	# This function will call alias witch is pointing to mbus data request
	# result or error will be returned
def getTheData():

	request = subprocess.Popen(["/bin/bash", "-i", "-c", "mbusReq"], stdout=subprocess.PIPE, shell=False)
	data, error = request.communicate()
	data = data.split()
	
	return data, error

#variables for next function uses
values = []
retData = []

valueNamesAndUnits = [
'Total Energy (kWh): ',
'Total Volume (m^3): ',
'VolumeFlow (liters): ',
'Power (kW): ',
'Flow temperature (Celcius): ',
'Return temperature (Celcius): ',
'Current Energy (kWh): '
]


	# this function will be called from readAllValues.py
		# Mbusdata will be handled by each value specific id 0 - 6
		# Handled values and their names will be returned
		# id(1) will be divided with value 1000 = m m^3 to m^3
		# id(3) will be divided with value 1000 = W to kW
		# id(4) and id(5) will be divided with value 10 so get Celcius values
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
				values[id] = values[id]/1000 #id = m^3 and 3 = kW
				
			elif id == 4 or id == 5:
				values[id] = values[id]/10 # id 4 and 5 = celcius
				
		for i in range(0,7):
			retData.append(valueNamesAndUnits[i] + str(values[i]))
			
		return retData
		
	else:
		return error