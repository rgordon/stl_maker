'''
Created on Oct 1, 2019

@author: ms
'''

def main_help():
    '''This is the help file for the program. The text below in "help_me" gets 
    pulled to become the help variable for the main program.'''
    help_me = '''
    This program creates an STL file based on the inputs provided in a config file.
		All of the inputs are described in the file: input.json
		
	To run this program, you will need a couple of additional python modules beyond the default stuff. In particular, you will need
	
	bitstring  ("pip install bitstring" from a command window)
	
	numpy ("pip install numpy" from a command window)
	
    '''
    return(help_me)