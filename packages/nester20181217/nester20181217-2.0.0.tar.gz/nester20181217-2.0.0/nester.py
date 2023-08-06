import sys
"""
这是“nester.py”模块，提供了一个名为 print_lol()的函数，这个作用是打印列表，其中有可能包吃住（也有可能不包含）嵌套列表	
"""
def print_lol(the_list,indent=False,level=0,fn=sys.stdout):
    """This function takes one positional argument called "the_list", which is any python list (of - possibly - nestted lists). Each data item in the provided list is (recursively) printed to the screen on it's own line."""
    for each_item in the_list:
        if isinstance(each_item, list):
             print_lol(each_item,indent,level+1,fn)
        else:
            if indent:
                for tab_stop in range(level):
                    print("\t",end='',file=fn)
            print(each_item)

def sanitize(time_string):
    if '-' in time_string:
        splitter = '-'
    elif ':' in time_string:
        splitter = ':'
    else:
        return(time_string)
    (mins,secs) = time_string.split(splitter)
    return(mins+'.'+secs)