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
import base64,sys



#TODO https://docs.apivoid.com/  this too  and finish the class


HTTP_METHODS = ["GET","POST","PUT","DELETE","PATCH","HEAD","OPTIONS","CONNECT","TRACE"]




def send_virustotal(api,url):
    # base64-url-safe encode (strip trailing '=')
    encoded_url = base64.urlsafe_b64encode(url.encode()).decode().rstrip("=")
    # Let's say you do a GET request to the URL's VirusTotal resource:
    url = f"https://www.virustotal.com/api/v3/urls/{encoded_url}"
    headers = {
        "x-apikey": api,
        "accept": "application/json"
    }
    response = requests.get(url, headers=headers)
    return response


def send_urlscan(api_key, url, visibility="public"):
    endpoint = "https://urlscan.io/api/v1/scan/"
    headers = {
        "API-Key": api_key,
        "Content-Type": "application/json"
    }
    payload = {
        "url": url,
        "visibility": visibility  # 'public' or 'private'
    }
    
    try:
        response = requests.post(endpoint, json=payload, headers=headers)
        response.raise_for_status()  # Raise error for non-2xx responses
        scan_result = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        sys.stdout.flush()
        return None
    
    
    # Extract scan UUID
    scan_uuid = scan_result.get("uuid")
    if not scan_uuid:
        print("Error starting scan:", scan_result)
        return None

    print(f"Scan started! UUID: {scan_uuid}")
    result_url = f"https://urlscan.io/result/{scan_uuid}/"
    print(f"View results here: {result_url}")

    # Wait for scan to complete with a max wait time
    result_endpoint = f"https://urlscan.io/api/v1/result/{scan_uuid}/"
    max_wait_time = 60  # Maximum wait time in seconds
    wait_interval = 5  # Polling interval
    elapsed_time = 0
    sys.stdout.flush()

    while elapsed_time < max_wait_time:
        time.sleep(wait_interval)
        elapsed_time += wait_interval
        result_response = requests.get(result_endpoint)

        if result_response.status_code == 200:
            return result_response.json()  # Return JSON result

    print("Scan results not available within the time limit.")
    sys.stdout.flush()
    return None

    

class API_Helper:
    def __init__(self,dbp):
        try:
            self.api_virustotal = dbp.check_or_get_data(table_name="API_Table",columns="value",condition="api_website_name",value="virustotal", message_type="condition")[0][0]
            self.api_urlscan = dbp.check_or_get_data(table_name="API_Table",columns="value",condition="api_website_name",value="urlscan", message_type="condition")[0][0]
            #Decrypt the API keys
            self.api_virustotal = self.__Decrypt__(self.api_virustotal)  
            self.api_urlscan = self.__Decrypt__(self.api_urlscan)
            sys.stdout.flush()
        except Exception as e:
            self.api_urlscan = None
            self.api_virustotal = None
            print(e)
            sys.stdout.flush()
            return None
        
        #print(self.api_virustotal)
        #print(self.api_urlscan)


        
        
    def __Decrypt__(self, API_KEY: str) -> str:
        try:
            private_key_path = Path(__file__).parent.parent.parent.parent / "keys" / "Private.pem"

            with open(private_key_path, "rb") as file:  # Open the private key file
                private_key = RSA.import_key(file.read())

            cipher_rsa = PKCS1_OAEP.new(private_key)  # Create a new PKCS1_OAEP object

            # Ensure API_KEY is a string and clean it up
            if isinstance(API_KEY, bytes):
                API_KEY = API_KEY.decode("utf-8")

            API_KEY = API_KEY.strip()  # Remove any extra whitespace

            # Fix incorrect Base64 padding
            missing_padding = len(API_KEY) % 4
            if missing_padding:
                API_KEY += "=" * (4 - missing_padding)

            try:
                encrypted_data = base64.b64decode(API_KEY, validate=True)
            except base64.binascii.Error as e:
                raise ValueError(f"Invalid Base64 encoding: {e}")

            decrypted_data = cipher_rsa.decrypt(encrypted_data)  # Decrypt the message
            return decrypted_data.decode("utf-8")  # Convert bytes to string

        except Exception as e:
            raise ValueError(f"Decryption failed: {e}")  # Raise error for better debugging


    


    def ScanURL(self,target_url) -> dict:
        print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        if target_url is None:
            return None
        print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        scan_results = {}
        try:
            virustotal_response = send_virustotal(self.api_virustotal,target_url)
            urlscan_response = send_urlscan(self.api_urlscan,target_url)
            
            #Extract the data from the responses
            scan_results["virustotal"] = self.extract_response_data(response=virustotal_response,api_type="virustotal") 
            scan_results["urlscan"] = self.extract_response_data(response=urlscan_response,api_type="urlscan")
            
            return scan_results
                 
        except Exception as e:
            print(e)
            sys.stdout.flush()
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
            sys.stdout.flush()
            return None            
                


            
        
    
        
"""
    

def replace_to_api(lines: list) -> list:
    updated_lines = []  # Store modified lines

    for line in lines:
        modified_parts = []  # Store modified parts of each line
                        
        for part in line.strip().split("|"):  # Split the line by '|'
            if "__replace_me__" in part:
                l = part.split(",")  # Split by ","
                if len(l) > 1:  # Ensure valid split
                    parts = l[1].split(":")  # Split second element by ":"
                    if len(parts) > 1:  # Ensure valid split
                        parts[1] = "work"  # Modify the second part
                        l[1] = ":".join(parts)  # Reconstruct
                    part = ",".join(l)  # Reconstruct the full segment
                            
            modified_parts.append(part)  # Add modified (or unmodified) part
                            
         
        updated_lines.append("|".join(modified_parts))  # Join modified parts
                    
                        
         
                    env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.env_user_db"))
                    cursor = connection.cursor()
                    
                    
                    with open(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../api_methods.txt")), "r") as fp:
                        lines = fp.readlines()  # Read all lines into a list
                    for line in lines:
                        line = line.split("|")
                        sql = "INSERT INTO API_Methods (url, api_name, http_method, headers) VALUES (%s, %s,%s,%s)"
                        vals = (line[0],line[1],line[2], line[3])
                        cursor.execute(sql, vals)
                        connection.commit()
    


"""

        
        
                
      
        
       


"""

if __name__ == "__main__":
    from General_Functions import read_ini_file #When I run the file directly
    from Database_Class import Database_Connection_Class #When I run the file directly
    pass
else:
    from app_data.Functions_and_Classes.General_Functions import read_ini_file #When I import the file to another file
    from app_data.Functions_and_Classes.Database_Class import Database_Connection_Class #When I import the file to another file
"""
