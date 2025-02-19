import requests
from web.api.Functions_and_Classes.General_Functions import *
from web.api.Functions_and_Classes.Database_class import Database_Connection_Class
from functools import wraps

#Encryption and Decryption modules
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import time
#This module converts binary data to Hexadecimal
from binascii import hexlify
import base64



#TODO https://docs.apivoid.com/  this too  and finish the class


HTTP_METHODS = ["GET","POST","PUT","DELETE","PATCH","HEAD","OPTIONS","CONNECT","TRACE"]




def send_http_request(self,headers:dict,url:str,http_method:str,payload:dict) -> any:
    try:
        match http_method.lower():
            case "post":
                response = requests.post(url, headers=headers,data=payload)
                if response.status_code == 200:
                    return response.json()
                return response.text
            case "get":
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    return response.json()
                return response.text
            case _:
                return None
    except Exception as e:
        print(e)
        
    
    
    


class API_Helper:
    def init(self):
        try:
            with Database_Connection_Class() as db_object: #in order to close the connection after using the class
                #Get the API keys from the database
                self.api_virustotal = db_object.check_or_get_data(table_name="API_Table",columns="value",condition="website_name",value="virustotal", message_type="condition")
                self.api_APIVoid = db_object.check_or_get_data(table_name="API_Table",columns="value",condition="website_name",value="APIVoid", message_type="condition")
                
            #Decrypt the API keys
            self.api_virustotal = self.__Decrypt_(self.api_virustotal)
            self.api_APIVoid = self.__Decrypt_(self.api_APIVoid)
        except Exception as e:
            print(e)
            return None
        
        #print(self.api_virustotal)
        #print(self.api_APIVoid)


        
        
        
    def __Decrypt_(self,API_KEY) -> str:
        try:
            private_key_path = Path(__file__).parent.parent.parent.parent / "Keys" / "Private.pem"
            with open(private_key_path, "rb") as file: #Open the private key file
                private_key = RSA.import_key(file.read())
                cipher_rsa = PKCS1_OAEP.new(private_key) #Create a new PKCS1_OAEP object with the private key
                decrypted_data = cipher_rsa.decrypt(API_KEY) #Decrypt the message
                #print(f"Decrypted: {decrypted_data.decode('utf-8')}") #Print the decrypted message
                
            return decrypted_data.decode('utf-8')
        except Exception as e:
            print(e)
            return None
       
    
    

    

    
    
    def Scan(self,**kwds) -> any:
        message = None
        headers = kwds.get("headers",None)
        APIType = kwds.get("api_type",None)
        url = kwds.get("url",None)
        http_method = kwds.get("http_method",None)
        payload = kwds.get("payload",None)
        
        if headers is None or APIType is None or url is None or http_method is None or self.api_virustotal is None or self.api_APIVoid is None:
            return None
        
        if http_method.upper() not in HTTP_METHODS: #Check if the http method is valid
            return None
        
        if APIType.lower() != "virustotal" or APIType.lower() != "APIVoid" :
            return None
            
    
        try:
            pass 
                
        except Exception as e:
            print(e)
            return None

        
    
    
    
       
       
    def extract_response_data(self,response,api_type) -> dict:
        if response is None or api_type is None:
            return None
        try:
            data = response.json()  # Convert the response to dict
        
            if api_type.lower() == "virustotal":
                # Navigate down to the attributes section:
                attributes = data.get("data",{}).get("attributes",{})                
                analysis_stats = attributes.get("last_analysis_stats",{})
                total_votes = attributes.get("total_votes",{})
                return {
                    "malicious_count":analysis_stats.get("malicious",-1),
                    "suspicious_count":analysis_stats.get("suspicious",-1),
                    "harmless_count":analysis_stats.get("harmless",-1),
                    "undetected_count":analysis_stats.get("undetected",-1),
                    "timeout_count":analysis_stats.get("timeout",-1),
                    "reputation":attributes.get("reputation",-1),   
                    "total-votes-harmless":total_votes.get("harmless",-1),
                    "total-votes-malicious":total_votes.get("malicious",-1),
                    "categories":attributes.get("categories",{})    
                           
                }
            elif api_type=="urlscan":
                page_info = response.get("page", {})
                url_status = response.get("verdicts", {}).get("overall", {})
                return {
                    "url:", page_info.get("url", "N/A"),
                    "domain:", page_info.get("domain", "N/A"),
                    "country:", page_info.get("country", "N/A"),
                    "malicious", url_status.get("malicious", False),
                    "score:", url_status.get("score", "N/A")
                }
                
            else:
                return None
            
            
        except Exception as e:
            print(e)
            return None            
                



                
            
        
    
        
        
        
        
                
      
        
       


"""

if __name__ == "__main__":
    from General_Functions import read_ini_file #When I run the file directly
    from Database_Class import Database_Connection_Class #When I run the file directly
    pass
else:
    from app_data.Functions_and_Classes.General_Functions import read_ini_file #When I import the file to another file
    from app_data.Functions_and_Classes.Database_Class import Database_Connection_Class #When I import the file to another file
"""
