__author__ = 'cwong_000'

import os
import slacker_config


class Run():
    def __init__(self):
        # hard code the function as string in this array
        self.services_strings = ['']
        num = 1
        #Retrieving the keys in the dictionary and store them into the list
        for key in slacker_config.urls.services_script_name:
            print(num + " for " + key + "\n")
            num += 1
            if key not in self.services_strings:
                self.services_strings.append(key)

    # Display the names of functions with its relevant number in self.services_strings
    def display_services_strings(self):

        temp_num = 1
        #Printing of the functions available to be called using run_services
        print("Functions available to be called using run_functions(value):\n")
        for i in self.services_strings:
            print(temp_num + " for " + i + "\n")
            temp_num += 1


    #Accept a value and use it to run the relevant functions in self.function_strings
    def run_services(self, value):
        #minus one as the array is zero-based
        value -= 1
        try:
            #use the given num to retrieve the service name
            selected_function = self.services_strings[value]
            #using the service name as a key to retrieve the directory path in the dictionary
            chdir_path = slacker_config.urls.services_path[selected_function]
            #change into that directory
            os.chdir(chdir_path)
            #run the script
            os.system('python ' + slacker_config.urls.services_script_name[selected_function] + '.py 0')
        except IndexError:
            print(
                "Number provided has no relevant functions, please enter a number between 1 to " + self.services_strings.__len__())




