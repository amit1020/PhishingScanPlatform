import sys,os,configparser,mysql.connector
from mysql.connector import Error
from datetime import datetime
from pathlib import Path
from General_Functions import read_ini_file



HTTP_METHODS = ["GET","POST","PUT","DELETE","PATCH","HEAD","OPTIONS","CONNECT","TRACE"]



sys.stdout.reconfigure(encoding='utf-8')



            
class Database_Connection_Class():
    def __init__(self,user_type):
        #self.database_code_path = Path(__file__).parent.parent / "DatabaseCode.sql"
        #self.database_code_path = "./Users_DB.sql"#!When I run the file directly
        self.database_code_path = "C:/Users/amitl/Documents/PhishingScanPlatform/app_data/Functions_and_Classes/Users_DB.sql" #!When I import the file to another file
        conenction_data = read_ini_file("Database_Connection",None)
   
        try: #set the setting of the connection frin the ini file
            self.connection = mysql.connector.connect(
                host=conenction_data['MYSQL_HOST'],
                user='root',
                password='dsmf9832bd238u0dj',
                port=conenction_data['MYSQL_PORT'],
                database=conenction_data['MYSQL_DATABASE'],
                charset='utf8mb4',
            )
        
            if self.connection.is_connected():
                self.mycursor = self.connection.cursor()
                self.Build_database()
        except Error as e:
            print(e)
            self.mycursor = None
            return None
    
    #*-------------------------------Get_Links----------------------------------------------------------------------------
    def Get_Links(self,api_method_type:str) -> dict: #Get the links from the database for Send_requests_api function
        if api_method_type is None:
            return []
        match api_method_type:
            case "url_scan":
                sql_command = "SELECT website_name,link,request_type,headers FROM Phishing_Database.Links_Table WHERE purpose='url_scan'"           
            case "threat_catagories":
                sql_command = "SELECT website_name,link,request_type,headers FROM Links_Table WHERE purpose='threat_catagories'"

            case "domain_scan":
                sql_command = "SELECT website_name,link,request_type,headers FROM Phishing_Database.Links_Table WHERE purpose='domain_scan'"
            case _:
                return []
        
        try:
            self.mycursor.execute(sql_command)
            results = self.mycursor.fetchall()
            rows = []
            for row in results:
              
                if len(row) == 4:
                    (website_name, link, request_type, headers) = row  # Unpack the tuple
                    rows.append({
                        "website_name": website_name,
                        "link": link,
                        "request_type": request_type,
                        "headers": headers
                    })
            return rows 
        except Exception as e:
            print(e)
            return None
    #*-----------------------------------------------------------------------------------------------------------
    
    #!Test function 
    def Get_Connection_Status(self):
        return self.connection.is_connected()
    
    
    
    
    
    #*-------------------------------Add_Links----------------------------------------------------------------------------
    def Add_Links(self,Data:dict) -> tuple[bool,str]:
        if Data is not None: #check if the data is not empty
            for item in Data.values():
                if item == "" or item == None: #check if there is an empty field, if there is return False
                    return (False,"There is an empty field")
            try:
                sql = "INSERT INTO Links_Table (purpose, website_name, link, request_type, description, headers) VALUES (%s, %s, %s, %s, %s, %s)"
                if Data['request_type'] not in HTTP_METHODS:
                    return (False,"The request type is not valid")
                
                vals = (Data['purpose'],Data['website_Name'],Data['link'],Data['request_type'],Data['description'],Data['headers'])
                
                self.mycursor.execute(sql,vals)
                self.connection.commit()
                
                return (True,f'Success to add new Link - {Data["link"]}')

            except Exception as error:
                return (False,f"Error to add new Link - {Data['link']} code problem:\n[!] {error}")
     #*-----------------------------------------------------------------------------------------------------------
     
     
     
     
     
     
    #*if the database isnt exist, the pythob will  Build the database from the sql file 
    def Build_database(self):
        with open(self.database_code_path, 'r',encoding='utf-8') as file: #read the sql file
            sql_commands = file.read()
        for command in sql_commands.split(';'):
            if command.strip():
                try:
                    self.mycursor.execute(command) #execute the command 
                    self.connection.commit()
                    print(f"Executed: {command}")
                except mysql.connector.Error as err:
                    print(f"Error: {err}")
                    self.connection.rollback()
    #*-----------------------------------------------------------------------------------------------------------                
                    
                    
                    
    #?NEED TO UNDERSTANT MORE                
    def close_connections(self):
        if hasattr(self, 'mycursor') and self.mycursor:
            self.mycursor.close()
        if hasattr(self, 'connection') and self.connection:
            self.connection.close()
            print("The connection is closed")
    #?NEED TO UNDERSTANT MORE
    def __enter__(self):
        return self
    #?NEED TO UNDERSTANT MORE
    def __exit__(self, exc_type, exc_value, traceback:bool):
        self.close_connections()
        
    
        
if __name__ == "__main__":
    from General_Functions import read_ini_file #When I run the file directly
    
    t = Database_Connection_Class("a")
    with Database_Connection_Class("a") as testing: #in order to close the connection after using the class
        '''
        result_bool,result=testing.Add_Links(
                            {"purpose":"threat_catagories",
                            "website_Name":"virustotal",
                            "link":"https://www.virustotal.com/api/v3/popular_threat_categories",
                            "request_type":"GET",
                            "description":"Retrieve a list of popular threat categories",
                            "headers":"accept:application/json"
                            })
        if result_bool:
            print("work")
            print(result)
        else:
            print(result)
            print("didn't work")
        
        '''
        
        print(testing.Get_Links("threat_catagories"))
        
        
else:
    pass
    #from app_data.Functions_and_Classes.General_Functions import read_ini_file #When I import the file to another file
                    



        
      
      








"""
    def Get_data_from_database(self,table_name:str,columns:str,condition:str=None,value:str=None,function_call_name:str=None):#Value is the value of the condition
        if self.mycursor is not None:
            if condition is not None and value is not None:
                try:
                    self.mycursor.execute(f"SELECT {columns} FROM {table_name} WHERE {condition}='{value}'")# get from the database all names of clients
                    results = self.mycursor.fetchall()
                    rows = []
                    for row in results:
                        rows.append(row)
                    Write_Database_Log(f"User get all columns: {columns} from {table_name} Table", "INFO")
                    
                    #FP = Fitness_perimetersTable, C = ClientsTable
                    if function_call_name is not None and (function_call_name == "Get_Data_About_Client_From_App_Page_C" or function_call_name == "Get_Data_About_Client_From_App_Page_FP"):
                        if function_call_name == "Get_Data_About_Client_From_App_Page_C": 
                            return dict(zip(PARAMS_FOR_GET_DATA_RETURN_ClientTable, rows[0])) 
                        
                        else: #function_call_name == "Get_Data_About_Client_From_App_Page_FP"
                            #TODO improve the code of all the function 
                            self.mycursor.execute(f"SELECT {columns} FROM {table_name} WHERE {condition}='{value}' ORDER BY Check_Date DESC LIMIT 1;")# get from the database all names of clients
                            results = self.mycursor.fetchall()
                            rows = []
                            for row in results:
                                rows.append(row)  
                            return dict(zip(PARAMS_FOR_GET_DATA_RETURN_Fitness_perimetersTable, rows[0]))
                    return rows
                except Exception as e:
                    print(e)
                    Write_Database_Log(f"{e}", "WARNING")
                    return None
            else:
                try:
                    self.mycursor.execute(f"SELECT {columns} FROM {table_name}")# get from the database all names of clients
                    results = self.mycursor.fetchall()
                    rows = []
                    for row in results:
                        rows.append(row)
                    #Write_Database_Log(f"User get all columns: {columns} from {table_name} Table", "INFO")
                    return rows
                except Exception as e:
                    #Write_Database_Log(f"{e}", "WARNING")
                    return None
        else:
            Write_Database_Log("The Curser not connect, Function Get_data_from_database ", "WARNING")
            print("cursor is not connect")

    
    
    def Searching_user(self,Phone_Number:str):
        if self.mycursor is not None:
            try:
                self.mycursor.execute(f"SELECT Phone_Number From ClientsTable WHERE Phone_Number={Phone_Number}")
                
                if len(self.mycursor.fetchall()) == 0: #result list
                    Write_Database_Log(f"There is not user - {Phone_Number}","WARNING")
                    return None
                else:
                    return True
            except Exception as e:
                Write_Database_Log(f"Problen to search user: {e}","ERROR")
                
            

    
    def Create_Client(self,Data:dict) -> bool:
        if Data is not None:
            try:
                sql = "INSERT INTO ClientsTable (FullName, Phone_Number, Address, Age, Gender, Begining_Date, Email, HEALTH_DECLARATION) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                vals = (Data['FullName'],Data['Phone_Number'],Data['Address'],Data['Age'],Data['Gender'],Data['Begining_Date'],Data['Email'],Data['HEALTH_DECLARATION'])
                self.mycursor.execute(sql,vals)
                self.connection.commit()
                Write_Database_Log(f"Success to add new client - {Data['FullName']}", "INFO")
                self.Create_Fitness_perimeters(Data=Data)
                print(f"Success to add new client - {Data['FullName']}")
                return True

            except Exception as error:
                print(f"Error to add new client - {Data['FullName']} code problem:\n[!] {error}")
                Write_Database_Log(f"Error to add new client - {Data['FullName']} code problem:\n[!] {error}", "ERROR")
                return False






   

#TODO Check why __del__ not work here
    def close_connections(self):
        try:
            if hasattr(self, 'mycursor') and self.mycursor:
                self.mycursor.close()
            if hasattr(self, 'connection') and self.connection:
                self.connection.close()
        except Exception as e:
            pass
"""




