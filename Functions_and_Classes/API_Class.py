import requests,configparser,csv


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
        config.read('../config.ini')
        # Access values
        self.api_key = config['api_virustotal']['api_key']
        self.endpoint = config['api_virustotal']['endpoint']
        # Set default headers
        self.headers = {
            "X-Apikey": self.api_key,
            "accept": "application/json",
            "content-type": "application/x-www-form-urlencoded"
        }




    def Send_requests_api(self,data,api_function):
        #data = {"url": endpoint}
        response = requests.post(url, headers=self.headers,data=data)
        if response.status_code == 200:
            return response.json()
        else:
            return response.text




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




    #data = [['Name', 'Age', 'City'], ['Alice', 30, 'New York'], ['Bob', 25, 'Los Angeles']]
