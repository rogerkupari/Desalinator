import sys, subprocess


# This program will be executed from graphical interface controller part (valves and motors)
	# program will call alias (wich is commanding the individual channe of relay, more information = see aliases)
	# system argument will be captured and its onward to be the alias word 
	

var = sys.argv[1]


subprocess.Popen(["/bin/bash", "-i", "-c", str(var)])
