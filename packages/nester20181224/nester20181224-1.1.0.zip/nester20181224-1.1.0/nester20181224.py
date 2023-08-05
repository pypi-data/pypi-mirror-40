def printi(array,level):
	for i in array:
		if  isinstance(i,list):
			printi(i,level+1)
		else:
                        for tab_stop in range(level):
                                print('\t',end='')
			print(i)
