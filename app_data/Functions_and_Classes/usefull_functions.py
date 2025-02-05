import configparser

"""
Check Current Execution Policy
    -Get-ExecutionPolicy -List

Change the Execution Policy
    - Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned

Return to noraml premishions
    - Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Restricted

    
    
    
"""


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

def Enter_cvsv_to_file(file_path, data):  
    import csv

    file_path = 'Functions_and_Classes\API_URLS.csv'
    
    name = "dsfsfs"


    with open("Functions_and_Classes\\test.txt", mode='r') as fd:
        for r in fd.readlines():
            print(r)
            r = r.split(",")
            print(r)
            try:
                data = [r[0],r[1],r[2],r[3], r[4]]
                with open(file_path, mode='a', newline='') as file:
                    csv_writer = csv.writer(file)
                    csv_writer.writerow([data])
            except:
                pass
            
            
            
            
            
