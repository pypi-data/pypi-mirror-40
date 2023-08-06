'''This is the tnestlist.py module, and it provide one function called
print_list() which print the lists that may or may not included nested lists'''

def print_list(the_list, level):
    '''This function takes a positional argument called "the_list" which
    is any python list(of, possibly, nested lists). Each data item in the
    provied list is (recusively) printed to the screen on its own line
    A second parameter called "level" is used to insert tab-stops when
    a nest list encountered'''
    for each_item in the_list:
        if isinstance(each_item, list):
            print_list(each_item, level+1)
        else:
            for tab_stop in range(level):
                print("\t", end='')
            print(each_item)
