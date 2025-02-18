import sys,os,configparser,mysql.connector,time
from mysql.connector import Error
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv


HTTP_METHODS = ["GET","POST","PUT","DELETE","PATCH","HEAD","OPTIONS","CONNECT","TRACE"]



sys.stdout.reconfigure(encoding='utf-8')



            
class Database_Connection_Class:
    def __init__(self):
        
        self.database_code_path = Path(__file__).parent / "Users_DB.sql"#local path
        # Load .env file correctly
        env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.env_user_db"))
        load_dotenv(env_path)
        


        self.host = os.getenv("MYSQL_HOST", "-----")
        self.user = os.getenv("MYSQL_USER", "------")
        self.password = os.getenv("MYSQL_PASSWORD", "------")
        self.port = int(os.getenv("MYSQL_PORT", "3306"))
        self.database = os.getenv("MYSQL_DATABASE", "------")
        self.connection = None

        self.connect_with_retry()


    #Try to connects the dayabase with multiple retries
    def connect_with_retry(self, retries=10, delay=5):
        for attempt in range(retries):
            try:
                #print(f" Attempting MySQL connection (Try {attempt + 1}/{retries})...")
                #creates the connection var 
                self.connection = mysql.connector.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    database=self.database,
                    port=self.port,
                    charset="utf8mb4"
                )
                
                if self.connection.is_connected():
                    #?If the connection is success, create the cursor and build the database
                    self.mycursor = self.connection.cursor()
                    self.Build_database()
                return
            except mysql.connector.Error as err:
                time.sleep(delay)
        #If the connection is unable to connect after multiple retries, raise an exception 
        raise Exception("MySQL is not available after multiple retries.")
    
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
    
    
    
    def Get_OTP(self,Name:str) -> bool:
        if Name is not None:
            try:
                self.mycursor.execute(f"SELECT 2FA_key FROM Users_Table WHERE name='{Name}'")# get from the database all names of clients
                results = self.mycursor.fetchall()
                if len(results) == 0:
                    return False
                return results[0][0]
            
            except Exception as e:
                print(e)
                return False
        return False
    

    
    def Get_user_data(self,table_name:str,columns:str,condition:str=None,value:str=None) -> list[dict]:
        if self.mycursor is not None:
            if condition is not None and value is not None:
                try:
                    self.mycursor.execute(f"SELECT {columns} FROM {table_name} WHERE {condition}='{value}'")# get from the database all names of clients
                    results = self.mycursor.fetchall()
                    rows = []
                    for row in results:
                        rows.append(row)
                    
                    return rows
                except Exception as e:
                    print(e)
                    return None
        return None
    
    
    
    #*-------------------------------Create user----------------------------------------------------------------------------
    def Create_Client(self,Data:dict,twoFA_key_var:str) -> bool:
        if Data is not None:
            try:
                sql = "INSERT INTO Users_Table (name, password, email, 2FA_key, phone_number) VALUES (%s, %s, %s, %s, %s)"
                vals = (Data['name'],Data['password'],Data['email'], twoFA_key_var, Data['phone'])
                            
                self.mycursor.execute(sql,vals)
                self.connection.commit()
                                
                #return f"Success to add new client - {Data['name']}"
                
                return True

            except Exception as error:
                print(f"{error}")
                #return f"Error to add new client - {Data['name']} code problem:\n[!] {error}"
        
                return False


    
    
    
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
        #print("Running database setup...")
        with open(self.database_code_path, 'r', encoding='utf-8') as file:
            sql_commands = file.read()

        for command in sql_commands.split(';'):
            if command.strip():
                try:
                    self.mycursor.execute(command)
                    self.connection.commit()
                except mysql.connector.Error as err:
                    #print(f"Error executing SQL: {err}")
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




