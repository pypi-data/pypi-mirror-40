def printi(array):
	for i in array:
		if  isinstance(i,list):
				printi(i)
		else:
			print(i)
