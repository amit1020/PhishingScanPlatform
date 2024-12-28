import requests,configparser

# Read the config file
config = configparser.ConfigParser()
config.read('config.ini')

# Access values
api_key = config['api']['api_key']
endpoint = config['api']['endpoint']

# Set headers
headers = {
    "X-Apikey": api_key,
    "accept": "application/json",
    "content-type": "application/x-www-form-urlencoded"
}

data = {"url": endpoint}

response = requests.post(endpoint, headers=headers,data=data)
if response.status_code == 200:
    print(response.json())
else:
    print("Error:", response.status_code)
    print(response.text)