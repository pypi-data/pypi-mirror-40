"""
a module consisting of one function print_lol(list)
"""
import sys

def print_lol(the_list, indent=False  , level=0, f_out=sys.stdout ):
    """this function prints a list which may contain lists
    as input a object that must be a list"""
    #another way to write a comment
    for each_item in the_list:
        if isinstance( each_item, list):
            print_lol( each_item,indent, level+1 , f_out)
        else:
            if indent == True:
                for tab_stop in range(level):
                    print("\t",end='', file=f_out)                 
            print(each_item, file=f_out)
 
