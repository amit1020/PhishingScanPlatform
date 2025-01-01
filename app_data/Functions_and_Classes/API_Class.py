import requests




#TODO https://docs.apivoid.com/  this too  and finish the class
def send_request(data,url):
    response = requests.post(url, headers=self.headers,data=data)
    if response.status_code == 200:
        return response.json()
    else:
        return response.text



class API_Helper:
    def __init__(self):
        #? currently I don't have any idea what to put here
        pass
        
       
      #*Privat function to connect and get/set data from the database
    def __ConnectionWithDatabase(self,database_action:str,api_action:str):
        """_summary_

        Args:
            database_action (str): which action to do with the database
            api_action (str): which action the user want to do with the APIs(for example: url_scan, url_scan_report, etc)
        Returns:
            _type_: _description_
        """
        try:
            with Database_Connection() as db_object: #in order to close the connection after using the class 
                mach database_action:
                    case "get_links":
                        data = db_object.Get_Links()
                        
                        #?Write the code to get the data from the database
                    case "set":
                        #!Set Vertifiction 
                        pass
                        
                    case _:
                        return None
                pass
                #!Write the code to connect to the database
                
        except Exception as e:
            print(e)
            return None    




    #TODO types for arguments like: api_action:str
    def Send_requests_api(self,data,api_function:str):
                
        #TODO mach-case
        
        
        
        response = requests.post(url, headers=self.headers,data=data)
        if response.status_code == 200:
            return response.json()
        else:
            return response.text




if __name__ == "__main__":
    from General_Functions import read_ini_file #When I run the file directly
    from Database_Class import Database_Connection_Class #When I run the file directly
    pass
else:
    from app_data.Functions_and_Classes.General_Functions import read_ini_file #When I import the file to another file
    from app_data.Functions_and_Classes.Database_Class import Database_Connection_Class #When I import the file to another file
                






