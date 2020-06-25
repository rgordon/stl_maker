'''
Created on Mar 7, 2019

@author: ms
'''
import logging
import datetime
import subprocess
#Turn on logging
log=logging.getLogger(__name__)



def can_cast_as_int(item):
    '''Return True if passed value can be cast as integer'''
    try:
        i = int(item)
        return True
    except:
        return False


def PrintDict(thing, indent=3, level=0):
    
    if type(thing) in (str, float,int):
            print(indent*level*" " + str(thing))
            return
        
    elif type(thing) in (bool,):
            print(indent*level*" " + str(thing))
            return
        
    elif type(thing) in (list,tuple):
        for element in thing:
            if type(element) is str:
                print(indent*level*" "+ element)
            else:
                PrintDict(element,indent, level+1)
                print("")
        return    
    
    elif isinstance(thing,dict):
        for key in thing.keys(): 
            if type(thing[key]) in (str,float,int,datetime.datetime, bool): 
                print(indent*level*" "+ key+ ": " + str(thing[key]))
            else:
                print(indent*level*" "+key)
                PrintDict(thing[key],indent, level+1)
        return    
    
    elif "OrderedDict" in str(type(thing)):
        for element in thing: 
            key = element.key()
            if type(thing[key]) is str: 
                print(indent*level*" "+ key+ ": " + thing[key])
            else:
                print(indent*level*" "+key)
                PrintDict(thing[key],indent, level+1)

        return        
            
    else: 
        print("Found something that is not an expected type. Found: "+str(type(thing)) ) 
        return
    
    
def DictToString(thing, indent = 20):
        return_string = "\n"+ \
                        indent*" "+'{:<30}'.format("KEY")+"\tVALUE\n"
        for key in thing.keys():
            return_string += indent*" "+'{:<30}'.format(key)+"\t"+ str(thing[key])+"\n"
        return return_string
    
    
def ProcessInputDict(user_input_dict, definition_dict, internal_dict, dict_type, level ):
    '''user_input_dict = asset, 
                                         definition_dict = thing, 
                                         internal_dict   = self,
                                         dict_type = "Asset"
                                         level = required'''
    field_name = definition_dict["field"]
    if level == "required" and definition_dict["field"] not in user_input_dict.keys():
        log.critical(level+" field ["+definition_dict["field"]+"] missing in "+dict_type+" ["+internal_dict["Name"]+"].")
        quit()

    if field_name in user_input_dict.keys():
        user_value = user_input_dict[field_name]
        if "type" in definition_dict.keys():
            result = CheckType(user_value, definition_dict["type"])
            if result[0] == 1:
                if result[1] == False:
                    log.critical("Value-type mismatch in "+level+" field ["+field_name+"] in "+dict_type+" ["+internal_dict["Name"]+"]. Type must be "+definition_dict["type"]+".")
                else: log.critical("Value-type validation issue: "+str(result[1]) + " in "+dict_type+" ["+internal_dict["Name"]+"].")
                quit()
            else: 
                user_value = result[1]
        
        if "choices" in definition_dict.keys():
            if "type" in definition_dict.keys():
                if definition_dict["type"] == "boolean":
                    if user_value =="True": user_value = True
                    elif user_value =="False": user_value = False
            elif user_value not in definition_dict["choices"]:
                log.critical("Value for field ["+field_name + "] in "+dict_type+" ["+internal_dict["Name"]+"] incorrect. Must be one of " +",".join(definition_dict["choices"]))
                quit()

        internal_dict[field_name] = user_value
        del user_input_dict[field_name]
        
    elif "default" in definition_dict.keys():
        internal_dict[field_name] = definition_dict["default"]
        
    return




def CheckType(value, var_type):
    '''If "value" conforns to expected type, return value, else retuen false'''
    if var_type == "float":
        cleaned_value = value.strip().strip("$")
        try:
            float(cleaned_value)
            return (0,float(cleaned_value))
        except:
            return (1, False)
        
    elif var_type == "percent":
        stripped_value = value.strip()
        if stripped_value[-1] == "%":
            cleaned_value = stripped_value.strip("%")
            try:
                float_value = float(cleaned_value)
                return (0,float_value/100)
            except:
                return (1, False)
        else:
            try:
                float_value = float(cleaned_value)
                return (0,float_value)
            except:
                return (1, False)
            
    elif var_type == "date":
        stripped_value = value.strip()
        try:
            date = datetime.datetime.strptime(stripped_value, "%m/%d/%Y")
            return (0,date)
        except:
            return (1, False)
        
    elif var_type == "boolean":
        stripped_value = value.strip()
        if stripped_value in ("Yes","YES","yes", "True", "TRUE","T"):
            return (0,"True")
        elif stripped_value in ("No","NO","no","False","FALSE", "F"):
            return (0,"False")
        else:
            return (1, False)
    
    elif var_type == "year range":
        # should be YYYY-YYYY, or "all"
        if value in ("All","all","ALL"):
            return (0,"all")
        #try to split on the "-"
        else:
            try:
                year_list = value.split("-")
                return_list = []
                for item in year_list:
                    if can_cast_as_int(item):
                            return_list.append(int(item))
                    else: return (1, False)
                return (0,sorted(return_list))
            except:
                return (1, False)
    
    elif var_type == "int":
        if can_cast_as_int(value):
            return (0, int(value))
        else: return (1, False)
        
        
        
        
        
        stripped_value = value.strip()
        if stripped_value in ("Yes","YES","yes", "True", "TRUE","T"):
            return (0,"True")
        elif stripped_value in ("No","NO","no","False","FALSE", "F"):
            return (0,"False")
        else:
            return (1, False)





    else: return (1,"unknown type [" + var_type +"]")
        
def IEX(command, quiet= False, silent=False):
		'''Execute command in new process and return result.'''
		pipe = subprocess.Popen(command,shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		output_buffer = pipe.communicate()
		console_error = str(output_buffer[1], 'utf-8') # stderr - convert to utf-8 string 
		console_output = str(output_buffer[0], 'utf-8') # stdout - convert to utf-8 string 
		if not silent:
			if not quiet: print("++ CONSOLE OUTPUT ++++++++++++++++++")
			print(console_output)
			if not quiet: 
				print("")
				print("++ CONSOLE ERROR++++++++++++++++++")
				print(console_error)
		if pipe.returncode != 0:
			return {"status": "fail", "reason":console_error,"return_code":pipe.returncode}
		else:
			return {"status": "success", "result": console_output, "return_code":pipe.returncode}