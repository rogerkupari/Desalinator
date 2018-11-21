import sys, json
from crontab import CronTab
import mysql.connector as my

# JSON printing is extra-important, without it user interface cannot read (and present) results

# this program will be called from graphical user interface / testBench / start test -button or stop test -button
	# System will capture system argument which controlling decisions of program
	# if argument is "1", system will delete the old tablename if exist (more information; see makeTables.py)
		#system will get the latest tableName from text file which will be used to get the time interval attribute value
			# time interval will be placed on cron routine specific every minute {time interval}
				# system will excecute testingProgram.py and its result will be written on /home/pi/desalinator_sw/lib/testruns/temporary/data.log
					# user interface will monitored this log file and will present the occured results
	# If the argument is "0" as "stop test button" the log file will written with nothing [empty]
		#and same writing process on tablename
		
	# So when user end this testdrive the database which WAS in use, the channels to use it again is gone.
		# results is still in database, but system cant use the same table without human based performance
			# with this way trying to make sure that, the user does not use same table with dofferent tests.


dbHost = '****'
dbDes = '****'
dbUser = '****'
dbPasswd = '****'


onoff = str(sys.argv[1])


def getInterval():
	ltable = open("/home/pi/desalinator_sw/lib/database_process/temporary/latestTable.txt", "r")
	tableName_raw = ltable.readlines()
	retVal = ""
	for c in tableName_raw:
		retVal += c
	tableName = retVal
	
	try:
		
		db = my.connect(host=dbHost, user=dbUser, password=dbPasswd, database=dbDes)
		c = db.cursor(buffered = True)

		cmd = ("SELECT time_interval from " + tableName)
		c.execute(cmd)
		result_raw = c.fetchall()[0]
		
		c.close()
		db.close()
		
		return int(result_raw[0])
		
	except Exception as e:
		sys.stderr.write(str(e))
		
def makeCron(addTime):

	user = CronTab(user='pi')
	task = user.new(command='python /home/pi/desalinator_sw/ui/testingProgram.py > /home/pi/desalinator_sw/lib/testruns/temporary/data.log')
	task.minute.every(addTime)
	user.write()
	
def deleteCron(parameter):
	if parameter == 0:
		user = CronTab(user='pi')
		user.remove_all()
		user.write()
		
		emptyLog = open('/home/pi/desalinator_sw/lib/testruns/temporary/data.log', "w")
		emptyLog.writelines(" ")
		emptyLog.close()
		
		removeLatestTable = open("/home/pi/desalinator_sw/lib/database_process/temporary/latestTable.txt", "w")
		removeLatestTable.writelines(" ")
		removeLatestTable.close()
		
	else:
		user = CronTab(user='pi')
		user.remove_all()
		user.write()
		
		emptyLog = open('/home/pi/desalinator_sw/lib/testruns/temporary/data.log', "w")
		emptyLog.writelines(" ")
		emptyLog.close()
	
	

on = {"cron": "on"}
off = {"cron": "off"}


if int(onoff) == 1:
	deleteCron(1)
	time = getInterval()
	makeCron(time)
	print (json.dumps(on))
	
else:
	deleteCron(0)
	print (json.dumps(off))