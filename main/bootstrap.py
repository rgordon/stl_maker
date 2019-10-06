'''
Created on Oct 1, 2019
Common Functions used to bootstrap the Up_squared_builder program. 
@author: ms
'''
import os, sys, json
from datetime import *
import logging

from help import main_help
import helpers

#Turn on logging
log=logging.getLogger(__name__)



class Create_config(dict):
    def __init__(self): 

        my_help = main_help()

        # Capture the starttime of this script
        self["start_time"] = datetime.now()
        self["start_time_string"] = self["start_time"].strftime("%Y%m%d_%H%M%S")

        # Identify the directory where this script was called from, and set up some other directories
        self["calling_dir"] = os.getcwd()                                 # Directory where the script was called from
        self["script_dir"] = os.path.dirname(os.path.realpath(__file__)).replace("main","")  # Directory where this script is located 

        # get the OS type
        if   os.name == "nt"    : self["os"] = "W"
        elif os.name == "linux" : self["os"] = "L" 
        elif os.name == "posix" : self["os"] = "l"
        else:                     self["os"] = os.name    
        
        # Set defaults for program controls
        self["program_controls"] = {
            "debug_v"   : False,
            "debug_vv"  : False,
            "logfile_threshold":"None", # "None" means do not log to file
            "logfile_path":os.path.join( self["calling_dir"],"log_" + self["start_time_string"] + ".txt"),
            "logconsole_threshold": "NOTSET" # Options: CRITICAL = 50, ERROR = 40, WARNING = 30, INFO = 20, DEBUG = 10,NOTSET = 0"
            }
        
        # Set defaults and initialization vlaues
        self["true_values"] =  (True, "True",  "true",  "TRUE",  "t", "T", "Y", "y", "Yes", "yes")
        self["false_values"] = (False,"False", "false", "FALSE", "f", "F", "N", "n", "No" , "no" )
        
        

        
        
    def Print(self, indent=0):
        print(indent*" "+'{:<30}'.format("KEY"),"VALUE")
        for key in self.keys():
            print(indent*" "+'{:<30}'.format(key),str(self[key]))
        return
    
    def ToString(self, indent=20):
        return_string = "\n"+ \
                        indent*" "+"CURRENT CONFIG variable VALUES\n"+ \
                        indent*" "+'{:<30}'.format("KEY")+"\tVALUE\n"
        for key in self.keys():
            return_string += indent*" "+'{:<30}'.format(key)+"\t"+ str(self[key])+"\n"
        return return_string
        
        
    
def ParseCommandLineVariables(config):
    if len(sys.argv)==1: # It means no input arguments given.
            print(main_help())
    else:
        args = sys.argv
        i=1
        while i < len(args):
            config["command_line"] = args
            if  args[i].lower in ("-h","-?","h","?"): 
                print(main_help())
                exit()
            elif args[i] in ("-file", "file", "-F", "f", "F", "-f", "config_file") :
                i = i + 1
                file = args[i]
                ProcessConfigFile(file_name = file, config = config)
            i=i+1
            
            
            
def ProcessConfigFile(file_name, config):
        
    log.info("Opening file :"+ str(file_name) )
    
    json_file = open(file_name, "r")
    json_string = json_file.read()
    json_file.close()
    try:
        config["user_input_file"] = dict(json.loads(json_string))
        #config.Print()
    except:
        log.critical("JSON Broken in requirements_file." + " Error: "+ str(sys.exc_info()[1]))
        quit()
    


def Seperate_program_controls(config):
    '''Moves "program_controls" out of the "user_input_file" dictionary and into it's own.'''
    if "user_input_file" in config.keys():
        if "program_controls" in config["user_input_file"].keys():
            keys = list(config["user_input_file"]["program_controls"])
            for key in keys:
                if key in ("debug_v","debug_vv"):
                    if config["user_input_file"]["program_controls"][key] in config["true_values"]:
                        config["user_input_file"]["program_controls"][key] = True
                    else: config["user_input_file"]["program_controls"][key] = False
                config["program_controls"][key] = config["user_input_file"]["program_controls"][key]
                del config["user_input_file"]["program_controls"][key]
            del config["user_input_file"]["program_controls"]
            
    # Promote a couple of commonly used program control parameters
    config["debug_v"]  = config["program_controls"]["debug_v"]
    config["debug_vv"] = config["program_controls"]["debug_vv"]
    
    return config["program_controls"]


