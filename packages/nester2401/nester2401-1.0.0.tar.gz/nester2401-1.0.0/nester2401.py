"""
a module consisting of one function print_lol(list)
"""
def print_lol(the_list):
    """this function prints a list which may contain lists
    as input a object that must be a list"""
    #another way to write a comment
    for each_item in the_list:
        if isinstance( each_item, list):
            print_lol( each_item )
        else:
            print(each_item)
 
