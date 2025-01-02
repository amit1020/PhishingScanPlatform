import configparser
from pathlib import Path


#TODO improve the secuirity
def read_ini_file(action,api_name) -> configparser.SectionProxy:
    if action == "api" and api_name != None: #Check if the action is to get the api key
        config = configparser.ConfigParser()
        
        config.read(Path(__file__).parent.parent / "config.ini" ) #get the path of the config file
        
        if "api" in api_name and api_name in config.sections(): #Check if the api name is in the config file
            return config['APIs'] #return the api key
        else:
            return None
        
    elif action == "Database_Connection" and api_name == None:
        config = configparser.ConfigParser()
        config.read(Path(__file__).parent.parent / "config.ini" )#found the path of the config file
        return config['mysql_database_for_connection']
        
        
    else:
        return None
    
        





