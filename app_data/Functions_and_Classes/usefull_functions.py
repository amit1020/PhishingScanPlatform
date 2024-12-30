import configparser

def ini_to_env(ini_file, env_file):
    config = configparser.ConfigParser()
    config.read("config.ini")
    print(config.sections())
   
    
    #with open(env_file, 'w') as env:
        for section in config.sections():
            
            for key, value in config.items(section):
                env.write(f"{key.upper()}={value}\n")

# שימוש
ini_to_env('./config.ini', '.env')

