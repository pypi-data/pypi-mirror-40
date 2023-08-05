#This is my first funciton in python. maybe is first~
def printLol(the_list):
    #we will call myself to find next list
    for eachLol in the_list:
            if isinstance(eachLol,list):
                printLol(eachLol)
            else:
                print(eachLol)
