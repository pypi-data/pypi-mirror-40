#This is my first funciton in python. maybe is first~
# v1.2.0 set default value for the second argument.
def printLol(the_list,level_flag=0):
    #we will call myself to find next list
    for eachLol in the_list:
    	if isinstance(eachLol,list):
    		printLol(eachLol,level_flag+1)
    	else:
    		for tab_stop in range(level_flag):
    			print("\t",end='')
    		print(eachLol)
