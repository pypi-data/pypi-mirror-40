"""This is the "nester-Zacsoft- module
  a module that defines a function print_lol() that prints out a list
  nested or not nested as a single list"""
def print_lol(the_list, indent=True, indentation=0):
        """This function takes a positional argument called "the_list", that
       which is a Python list (of possibly nested list) It checks if the list we passed
           is a nested list or  not and each data item in the provided list is
           recusrsively printed to the screen on its own line.
           the argument "indentation" defines the number of tab stops used for indentation of lists"""
        for each_item in the_list:
            if isinstance(each_item, list):
                print_lol(each_item, indent, indentation+1)
            else:
                if indent:
                    for tab_stop in range(indentation):
                        print("\t", end='')
                print(each_item)
