import requests,configparser


#TODO https://docs.apivoid.com/  this too  and finish the class
def send_request(data,url):
    response = requests.post(url, headers=self.headers,data=data)
    if response.status_code == 200:
        return response.json()
    else:
        return response.text



class API_Helper:
    
    urls_api_function_dict = {  # Dictionary of API functions and their respective URLs
        "url_scan" : "https://www.virustotal.com/api/v3/urls", #POST - Submit a URL for scanning
        "domain_scan" : "https://www.virustotal.com/api/v3/domains/id/analyse", #POST - Retrieve a URL scan report
        "Threat_catagories" : "https://www.virustotal.com/api/v3/popular_threat_categories", #GET - Retrieve a list of popular threat categories
    }
    
    def __init__():
        # Read the config file
        config = configparser.ConfigParser()
        config.read('../config.ini') #TODO: Change this to the correct path with PATHLIB
        # Access values
        self.api_key = config['api_virustotal']['api_key']
        # Set default headers
        self.headers = {
            "X-Apikey": self.api_key,
            "accept": "application/json",
            "content-type": "application/x-www-form-urlencoded"
        }




    def Send_requests_api(self,data,api_function):
        response = requests.post(url, headers=self.headers,data=data)
        if response.status_code == 200:
            return response.json()
        else:
            return response.text








