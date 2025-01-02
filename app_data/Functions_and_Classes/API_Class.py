import requests,threading



#TODO https://docs.apivoid.com/  this too  and finish the class


HTTP_METHODS = ["GET","POST","PUT","DELETE","PATCH","HEAD","OPTIONS","CONNECT","TRACE"]

def send_request(payload,url,headers,request_type,my_lock):
    with my_lock:
        try:
            match request_type:
                case "post":
                    response = requests.post(url, headers=headers,data=payload)
                    if response.status_code == 200:
                        return response.json()
                    else:
                        return response.text
                case "get":
                    response = requests.get(url, headers=headers,params=payload)
                    if response.status_code == 200:
                        return response.json()
                    else:
                        return response.text
                case "put":
                    response = requests.put(url, headers=headers,data=payload)
                    if response.status_code == 200:
                        return response.json()
                    else:
                        return response.text
                    
                case _:
                    pass
        except Exception as e:
            print(e)
            return None




class API_Helper:
    def init(self):
        self.lock = threading.Lock()
        #? currently I don't have any idea what to put here
        pass
        
       
       
       
    #*Privat function to connect and get/set data from the database
    def __ConnectionWithDatabase(self,database_action:str,api_action:str) -> list[dict]:
        """_summary_

        Args:
            database_action (str): which action to do with the database, it can be(currently):
                -get_links
                -set
            api_action (str): which action the user want to do with the APIs, it can be(currently):
                -url_scan
                -threat_catagories
                -domain_scan
        Returns:
            _type_: _description_
        """
        try:
            with Database_Connection_Class() as db_object: #in order to close the connection after using the class 
                match database_action:
                    case "get_links":
                        return db_object.Get_Links(api_method_type=api_action)

                    case "set":
                        
                        #!Set Vertifiction 
                        pass
                        
                    case _:
                        return None
                    
                
                
                #!Write the code to connect to the database
                
        except Exception as e:
            print(e)
            return None    

#TODO types for arguments like: api_action:str
    def Send_requests_api(self,payload,api_function:str):
        threads = []
        try:
            payload = "Get_from_GUI"
            links = self.__ConnectionWithDatabase("get_links",api_function)#get the links from the database
            
            if links is not None:#if the links are not None
                for link in links: #run the links and send the requests
                    if link["request_type"] in HTTP_METHODS:
                        threads.append(threading.Thread(target=send_request,args=(payload,link["url"],link["headers"],link["request_type"],self.lock)))
                    else:
                        print("The HTTP method is not valid")
                        return None
                
                
                for thread in threads:
                    thread.start()
                
                for thread in threads:
                    thread.join()
                
        except Exception as e:
            print(e)
            return None
                
            
        
    
        
        
        
        
                
      
        
       




if name == "main":
    from General_Functions import read_ini_file #When I run the file directly
    from Database_Class import Database_Connection_Class #When I run the file directly
    pass
else:
    from app_data.Functions_and_Classes.General_Functions import read_ini_file #When I import the file to another file
    from app_data.Functions_and_Classes.Database_Class import Database_Connection_Class #When I import the file to another file


