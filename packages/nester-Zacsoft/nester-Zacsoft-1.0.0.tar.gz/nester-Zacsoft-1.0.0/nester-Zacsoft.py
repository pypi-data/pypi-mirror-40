"""This is a module
   that prints out a nested list
   as a single list"""
def print_lol(the_list):
        """This function checks if the list we passed
           is a nested list or  not,
           if not prints it out"""
        for each_item in the_list:
            if isinstance(each_item, list):
                print_lol(each_item)
            else:
                print(each_item)
