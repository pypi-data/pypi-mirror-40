#This is my first funciton in python. maybe is first~
def printLol(the_list,level_flag):
    #we will call myself to find next list
    for eachLol in the_list:
    	if isinstance(eachLol,list):
    		printLol(eachLol,level_flag+1)
    	else:
    		for tab_stop in range(level_flag):
    			print("\t",end='')
    		print(eachLol)
