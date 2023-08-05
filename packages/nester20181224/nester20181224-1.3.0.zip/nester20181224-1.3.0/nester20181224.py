def printi(array, indent = False, level = 0):
    for i in array:
        if  isinstance(i,list):
            printi(i, indent, level+1)
        else:
            if indent:
                for tab_stop in range(level):
                    print('\t',end='')
            print(i)
