#!/usr/bin/env python3

'''
Created on Oct 2, 2019
This set of code is a "stub" for building new programs. It contains a bunch of stuff I always use.
1. Bootstrapper to collect system, directories, etc.
2. Reader of a user input input JSON file. The file contains a space for user inputs and several program controls.
   ALl of these will end up in a dictionary called "config". The complete command line will end up in this dictionaly also.
3. Initializes python logging for console and file output.

@author: ms
'''

# import system modules
import os
import datetime
import logging
import math

# Import from this package
import bootstrap
import helpers





# BOOTSTRAP THE SCRIPT

# Call a function that creates a custom dictionary called "config" 
# that is used throughout the program. 
config = bootstrap.Create_config()


# Call a bootstrap function that processes the command line variables 
# and and reads in a user config file, putting the contents into the 
# "config" dictionary in two sub-dictionaries: 
# "program controls" : contains debug, logging, etc info 
# "user_input_file" : evertything not in "program controls"  
bootstrap.ParseCommandLineVariables(config)
program_controls = bootstrap.Seperate_program_controls(config)


#---------------------------------------------------------------------
# LOGGING SETUP

# Create a logger to grab ALL messages
log = logging.getLogger()
log.setLevel(40) # Set the level to only Errors and higher

# Create a formatter for use in all log output
formatter = logging.Formatter("%(asctime)s  %(levelname)-8s  "+\
                              "%(name)s\n" + 25*" "+"%(message)s")

#Create a log StreamHandler for writing to the console
console_handler = logging.StreamHandler()
console_handler.setLevel(30)
console_handler.setFormatter(formatter)
log.addHandler(console_handler)

# First, redefine the level for general use to 0
log.setLevel(0)

# Now look in the program controls for user resets to the logging levels
console_handler.setLevel(program_controls["logconsole_threshold"])
log.info("Current console logging level is: "+str(program_controls["logconsole_threshold"]))

# Set up logging to a file, if requested
if program_controls["logfile_threshold"] in ("CRITICAL", "ERROR", "WARNING", "INFO" , "DEBUG" ,"NOTSET"): 
    print("Setting up logging to file...")

    # Create a log handler for writing to the log file 
    # which logs everything (Level 0)
    file_handler = logging.FileHandler(program_controls["logfile_path"])
    file_handler.setLevel(program_controls["logfile_threshold"])
    file_handler.setFormatter(formatter)
    log.addHandler(file_handler)
    
log.info("Current file logging level is: "+str(program_controls["logfile_threshold"]))

log.info(config.ToString())



##################################################
#  START PROGRAM WORK
##################################################

#-------------------------------------------------


















