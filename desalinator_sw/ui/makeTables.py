import sys, json
import mysql.connector as my


#THIS program will be called from grapphical user interface / testBench / "make test" -form submit button
	#System will define the databases and store the given test attributes in future use
	
	# JSON printing is extra-important, without it user interface cannot read (and present) results


	#paths to names of attribute database columns (desalination_test_attr)
	#paths to names of storage columns (desalination)
attributes_columns_path = '/home/pi/desalinator_sw/lib/database_process/configurations/attribute_columns.txt'
storage_columns_path = '/home/pi/desalinator_sw/lib/database_process/configurations/storage_columns.txt'

	#Databaseinformation
dbHost = '****'
dbDes = '****'
dbDes2 = '****'
dbUser = '****'
dbPasswd = '****'

	#Database columns configuration variables
float42 = ' float(4,2), '
float52 = ' float(5,2), '
float51 = ' float(5,1), '
float73 = ' float(7,3), '
float62 = ' float(6,2), '
float53 = ' float(5,3), '
float32 = ' float(3,2), '
tf = ' BOOLEAN, '
txt = ' TEXT, '
commaonly = ', '


	# This function will be read and return attribute and storage columns
def databaseColumns():
	attributes = open(attributes_columns_path)
	attr_raw = attributes.readlines()
	attr = map(str.strip, attr_raw)
	
	storage = open(storage_columns_path)
	storage_raw = storage.readlines()
	stor = map(str.strip, storage_raw)
	
	attributes.close()
	storage.close()

	return attr, stor

	# this function will create the table of attributes in ..test_attr database
def createAttrTable(tableName):
		# see the order of variables by lib/database/configurations included files
	attribute, storage = databaseColumns()
	
	try:
		db = my.connect(host=dbHost, user=dbUser, password=dbPasswd, database=dbDes2)
		c = db.cursor(buffered = True)
		cmd = ("""
		CREATE TABLE """ + tableName + """ (
		id INT NOT NULL AUTO_INCREMENT, """ +
		
		attribute[0] + float42 +
		attribute[1] + float42 +
		attribute[2] + float42 +
		"""PRIMARY KEY (id)
		)""");
		c.execute(cmd)
		
		db.commit()
		c.close()
		db.close()
		
		
		return True

	except Exception as e:
		sys.stderr.write(str(e))
		return False
	

		# this function will create the storage "test values storage" in desalination database
def makeStorageTable(tableName):
	# see the order of variables by lib/database/configurations included files
	attribute, storage = databaseColumns()
	
	try:
		db = my.connect(host=dbHost, user=dbUser, password=dbPasswd, database=dbDes)
		c = db.cursor(buffered = True)
		cmd = ("""
		CREATE TABLE """ + tableName + """ (
		id INT NOT NULL AUTO_INCREMENT, """ +
		
		storage[0] + float52 +
		storage[1] + float52 +
		storage[2] + float52 +
		storage[3] + float52 +
		storage[4] + float52 +
		storage[5] + float52 +
		storage[6] + float52 +
		storage[7] + float52 +
		storage[8] + float52 +
		storage[9] + float52 +
		storage[10] + float52 +
		storage[11] + float52 +
		storage[12] + float62 +
		storage[13] + float73 +
		storage[14] + float51 +
		storage[15] + float53 +
		storage[16] + float52 +
		storage[17] + float52 +
		storage[18] + float52 +
		storage[19] + tf +
		storage[20] + tf +
		storage[21] + float32 +
		storage[22] + float32 +
		storage[23] + float32 +
		
		storage[24] + txt +
		storage[25] + txt +
		storage[26] + txt +
		storage[27] + txt +
		storage[28] + txt +
		storage[29] + txt +
		storage[30] + txt +
		storage[31] + txt +
		"""PRIMARY KEY (id)
		)""");
		c.execute(cmd)
		
		db.commit()
		c.close()
		db.close()
		
		
		return True

	except Exception as e:
		sys.stderr.write(str(e))
		return False
		
	# this function will put attribute values on ...test_attr database
def insertAttributes(tableName, hi, lo, time):	
	attribute, storage = databaseColumns()
	
	try:
		db = my.connect(host=dbHost, user=dbUser, password=dbPasswd, database=dbDes2)
		c = db.cursor(buffered = True)
		cmd = ("""INSERT INTO """ + 
		tableName 
		+ 
		""" 
		( """+
		attribute[0] + commaonly +
		attribute[1] + commaonly +
		attribute[2] +  
		""") 
		VALUES (%f, %f, %f)"""%(float(hi), float(lo), float(time)));
		c.execute(cmd)
		#print '"'+ tableName +'"' + "  table has done in database "
		
		db.commit()
		c.close()
		db.close()	
		
		return True

	except Exception as e:
		sys.stderr.write(str(e))
	
		
	
	# system argument catching
tableName = str(sys.argv[1])
vacuum_hi = str(sys.argv[2])
vacuum_lo = str(sys.argv[3])
interval = str(sys.argv[4])


	# if tables is created with no errors
		# attributes will be saved in database
			# latest name of table (wich is same on both databases [desalination] and [desalination_test_attr]) will be saved on text file
if createAttrTable(tableName):
	if makeStorageTable(tableName):
		if insertAttributes(tableName, vacuum_hi, vacuum_lo, interval):
			file = open("/home/pi/desalinator_sw/lib/database_process/temporary/latestTable.txt", "w") 
			file.writelines(str(tableName)) 
			file.close()
			toClient = {"topic": "Database tables Done", "interval": int(interval)}
			print (json.dumps(toClient))
		
	
	


