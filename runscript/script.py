__author__ = 'cwong_000'

import os


class script():
    def __init__(self):
        # hard code the function as string in this array
        self.functions_strings = ['']
        self.num = 1

    #Add function file name into the list
    def add_function(self, name):
        if name not in self.functions_strings:
            self.functions_strings.append(name)

    # Display the names of functions with its relevant number in self.function_strings
    def display_functions_strings(self):
        num = 1
        #Printing of the functions available to be called using run_functions
        print("Functions available to be called using run_functions(value):\n")
        for i in self.functions_strings:
            print(self.num + " for " + i + "\n")
            num += 1

    #Accept a value and use it to run the relevant functions in self.function_strings
    def run_functions(self, value):
        #minus one as the array is zero-based
        value -= 1
        try:
            run_function = 'python ' + self.functions_strings[value] + '.py 0'
            os.system(run_function)
        except IndexError:
            print(
                "Number provided has no relevant functions, please enter a number between 1 to " + self.functions_strings.__len__())
