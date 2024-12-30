import configparser
from pathlib import Path




#TODO improve the secuirity
def read_ini_file(action,api_name) -> configparser.SectionProxy:
    if action == "api" and api_name != None:
        config = configparser.ConfigParser()
        config.read(Path(__file__).parent.parent / "config.ini" ) #get the path of the config file
        
        if "api" in api_name and api_name in config.sections():
            return list(config[api_name]['api_key'])
        
        else:
            return None
        
    elif action == "database_Connection" and api_name == None:
        config = configparser.ConfigParser()
        config.read(Path(__file__).parent.parent / "config.ini" )
        db_config = config['mysql_database_for_connection']
        print(db_config['MYSQL_DATABASE'])
        
        
        return db_config
        
    else:
        return None
    
        
    




