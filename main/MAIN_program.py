#!/usr/bin/env python3

'''
Created on June 12, 2020
This is my attempt to write a tool to create stl files of surfaces defined by  Z as a function of X and Y.


This  program is built off my program stub.
	1. Bootstrapper to collect system, directories, etc.
	2. Reader of a user input input JSON file. The file contains a space for user inputs and several program controls.
	   ALl of these will end up in a dictionary called "config". The complete command line will end up in this dictionaly also.
	3. Initializes python logging for console and file output.

@author: ms
'''

# import system modules
import os
import logging
import math
from datetime import *
from pathlib import Path


# Import from this package
import bootstrap
import helpers
import stl_builder





# BOOTSTRAP THE SCRIPT

# Call a function that creates a custom dictionary called "config" 
# that is used throughout the program. 
config = bootstrap.Create_config()


# Call a bootstrap function that processes the command line variables 
# and reads in a user config file, putting the contents into the 
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

if config["debug_vv"]:
	log.info("Current console logging level is: "+str(program_controls["logconsole_threshold"]))

# Set up logging to a file, if requested via the config file
if program_controls["logfile_threshold"] in ("CRITICAL", "ERROR", "WARNING", "INFO" , "DEBUG" ,"NOTSET"): 
    print("Setting up logging to file...")

    # Create a log handler for writing to the log file 
    # which logs everything (Level 0)
    file_handler = logging.FileHandler(program_controls["logfile_path"])
    file_handler.setLevel(program_controls["logfile_threshold"])
    file_handler.setFormatter(formatter)
    log.addHandler(file_handler)

if config["debug_vv"]:
	log.info("Current file logging level is: "+str(program_controls["logfile_threshold"]))

if config["debug_v"]:
	log.info(config.ToString())



##################################################
#  START PROGRAM WORK
##################################################

#-------------------------------------------------

# Move inputs into variables
expected_inputs = ("Z_as_a_function_of_X_and_Y",
					"min_x",
					"max_x",
					"num_x_steps",
					"min_y",
					"max_y",
					"num_y_steps",
					"output_type",
					"output_filename",
					"output_directory")
					
user_inputs = config["user_input_file"]
for item in expected_inputs:
	if item not in user_inputs.keys():
		log.critical("Missing input in config file: " + item)
		quit()
	
Z_as_a_function_of_X_and_Y = user_inputs["Z_as_a_function_of_X_and_Y"]["Z_as_a_function_of_X_and_Y"]
min_x	 					= 	user_inputs["min_x"]["min_x"]
max_x				  	    = 	user_inputs["max_x"]["max_x"]
num_x_steps				    = 	user_inputs["num_x_steps"]["num_x_steps"]
min_y					    = 	user_inputs["min_y"]["min_y"]
max_y					    = 	user_inputs["max_y"]["max_y"]
num_y_steps				    = 	user_inputs["num_y_steps"]["num_y_steps"]
output_type					= 	user_inputs["output_type"]["output_type"]
output_filename				= 	user_inputs["output_filename"]["output_filename"]
output_directory			= 	user_inputs["output_directory"]["output_directory"]

#########################################################################################################
#Validate inputs
if   output_type in ( "text", "txt", "TEXT", "TXT", "Text"):         output_type = "txt"
elif output_type in ("binary", "bin","BINARY","BIN","Binary","Bin"): output_type = "bin"
else:
	log.critical("output_type in json ["+output_type+"] file not recognized")
	quit()

# create the output directory if it doesn't exist:
out_path = Path(output_directory)
out_path.mkdir(parents=True, exist_ok=True)
file_path = out_path / f'{output_filename}.stl'
# i think it still needs to be a string elsewhere in this code so keep it that way for now.
filepath = str(file_path.absolute())
"


#########################################################################################################
# Print some starting fluff
total_facets_expected = 2* num_x_steps*num_y_steps
print("Starting to caclulate a total of "+ str(total_facets_expected)+" triangular facets.")
duration_estimate_printed = False



#########################################################################################################
#Create and write the file header

#Set up the output file
stl_builder.Initialize_stl_file(filepath, output_type, total_facets_expected, solid_name = "")

# Create the file

# Append the required stl header info







#########################################################################################################
#Iterate over a grid of X and Y values defiend by the imput prarmeters
x_step = (max_x - min_x)/num_x_steps
y_step = (max_y - min_y)/num_y_steps
num_facets = 0


# Do one row of Y at a time 
last_row_values = []
for j in range(num_y_steps+1):
	y=min_y + j*y_step
	
	# make an array to collect a list of the Z values at each X for this Y
	this_row_values = []
	
	
	# Now step through the X locations
	for i in range (num_x_steps+1):
		x = min_x + i * x_step
		exec(Z_as_a_function_of_X_and_Y) # JASON file supplied code that delivers a variable named "z"
		this_row_values.append((x,y,z))
		
	if len(last_row_values) == 0: # check to see if this is the first row.
		last_row_values = this_row_values
		continue   
	
	else: # we have two wors of values, so we can proceed to build the triangular facets of our stl.
	
		#Step throught the arrays, building two triangles at each step
		for i in range (num_x_steps):
			first_triangle_points  =  (this_row_values[i], this_row_values[i+1], last_row_values[i])
			second_triangle_points =  (this_row_values[i+1], last_row_values[i+1], last_row_values[i] )
			#Create stl_facets for these two triangles
			first_stl_facet = stl_builder.STL_Facet(this_row_values[i], this_row_values[i+1], last_row_values[i])
			second_stl_facet =  stl_builder.STL_Facet(this_row_values[i+1], last_row_values[i+1], last_row_values[i] )
			
			#add these facets to the file
			first_stl_facet.Append_facet_to_file(filepath, output_type)
			second_stl_facet.Append_facet_to_file(filepath, output_type)
			
			# Increment facet count
			num_facets += 2
			
			if not duration_estimate_printed:
				if num_facets > 20:
					duration_so_far = datetime.now() - config["start_time"]
					time_per_facet = duration_so_far/num_facets
					remaining_facets = total_facets_expected - num_facets
					time_remaining = remaining_facets*time_per_facet
					expected_finish_time = datetime.now() + time_remaining
					print("Estimated calculation duration = "+str( time_remaining))
					print("Estimated completion time = "+str(expected_finish_time))
					duration_estimate_printed = True
		
		
		#We've processed each triangle, so lets move to the next row 
		last_row_values = this_row_values
	
print("stl creation complete. "+str(num_facets)+ " facets created'")
	
	
	
	
	
		








