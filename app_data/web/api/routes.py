from flask import (
    Blueprint, render_template, request,jsonify
)

import sys, os,json,re,requests


#Define the blueprint: 'product', set its url prefix: app.url/product
API_bp = Blueprint('API_bp', __name__)

try:
    from web.api.Functions_and_Classes.API_Class import API_Helper
    from web.api.Functions_and_Classes.General_Functions import *
    from web.api.Functions_and_Classes.Database_class import Database_Connection_Class
    
    my_db = Database_Connection_Class()#Create an instance of the Database_Connection_Class
    
except ImportError as e:
    print(f"Error importing Database_Class: {e}", file=sys.stderr)
    sys.exit(1)



def is_ValidURL(url) -> bool:
    # Check the URL begins with http:// or https://
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url  # Default to https if no scheme is provided

    # Check the URL format
    regex = re.compile( 
    r'^(https?:\/\/)?'  
    r'(([A-Za-z0-9-]+\.)+[A-Za-z]{2,6})'  # Domain name (e.g., example.com)
    r'(\/[^\s]*)?$'  # Optional path (e.g., /page)
    )
    if not re.match(regex, url):
        return False #, "Invalid URL format"

    try:#Check if the URL is reachable (real website check)
        response = requests.head(url, timeout=5, allow_redirects=True)
        if response.status_code < 400:  # Success (2xx or 3xx status codes)
            return True #, "URL is valid and online"
        else:
            return False #, f"URL responded with status code {response.status_code}"
    except requests.RequestException:
        return False # ,"URL is unreachable"

    



@API_bp.route('/test', methods=['GET'])
def product_home():
    return "hello world"
    
    
@API_bp.route('/Vertification/2FA', methods=['POST'])
def Vertification_2FA():
    try:
        data = request.get_json()
        print(data)
        # Ensure data is a dictionary
        if not isinstance(data, dict):
            return jsonify({"error": "Invalid data format, expected an object"}), 400

        username = data.get("username")
        otp = data.get("otp")

        if not username or not otp:
            return jsonify({"error": "Missing required fields"}), 400

        result =my_db.Get_OTP(Name=username)
        
        if result == None:
            return jsonify({"error": "User not found"}), 404
        
        
        if verify_otp(result, int(otp.strip())):
            return jsonify({"status": "Success"}), 200
        else:
            return jsonify({"status": "Failure"}), 401
                

      

    except Exception as e:
        print(str(e), file=sys.stderr)
        return jsonify({"error": str(e)}), 500


    
    
@API_bp.route('/add_user/', methods=['POST'])
def add_user():
    
    if request.method == 'POST':
        try:
            data = request.get_json()#Extract the data from the request
            # Ensure data is a dictionary (not a list)
            if not isinstance(data, dict):
                return jsonify({"error": "Invalid data format, expected an object"}), 400

            key = generate_2fa_secret() 
            
            result = my_db.Create_Client(Data=data, twoFA_key_var=key)#Creates the user, return True id successful, False if not

            if not result:  
                return jsonify({"error": "User creation failed"}), 400  

            return jsonify({"2FA_key": key, "message": "User created successfully"}), 200  #Return the key to the user for connect the 2FA app

        except Exception as e:
            #!Change the error message
            return jsonify({"error": str(e)}), 500  
    
    return jsonify({"error": "Invalid request method"}), 405


@API_bp.route('/ScanURL/', methods=['POST'])
def ScanURL():
    if request.method == 'POST':
        
        try:
            data = request.get_json()#Extract the data from the request
            if not isinstance(data, dict):
                #!Change the error message
                return jsonify({"error": "Invalid data format, expected an object"}), 400
            target_url = data.get("url")
            
        
            if not is_ValidURL(target_url):
                return jsonify({"error": "Invalid URL"}), 400
            
            result = None
            print("hello",flush=True)
            my_api = API_Helper(dbp=my_db)#Create an instance of the API_Helper
            print("hello",flush=True)
            #result = my_api.ScanURL(target_url=target_url)#Scan the URL
            
            sys.stdout.flush()  # Ensures the buffer is flushed immediately
            print(result)

            while result is None:
                time.sleep(5)
            return jsonify({"status": "Success"}), 200
            
        except Exception as e:
            #!Change the error message
            #return jsonify({"error": "ERROR"}), 500
            return jsonify({"error": str(e)}), 500
        #https://www.google.com
        
    else:
        print("here")
        #!Change the error message
        return jsonify({"error": "Invalid request method"}), 405
    

        
"""

import requests



r = requests.post(data={'name': 'Alice', 'age': 25}, url='http://127.0.0.1:1234/api/add_user')


if r.status_code == 200:
    print(r.text)
else:   
    print('Error:', r.status_code)

"""