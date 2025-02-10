from flask import (
    Blueprint, render_template, request,jsonify
)

import sys, os,json


#Define the blueprint: 'product', set its url prefix: app.url/product
API_bp = Blueprint('API_bp', __name__)

try:
    from web.api.Functions_and_Classes.General_Functions import *
    from web.api.Functions_and_Classes.Database_class import Database_Connection_Class

    my_db = Database_Connection_Class()#Create an instance of the Database_Connection_Class
    
except ImportError as e:
    print(f"Error importing Database_Class: {e}", file=sys.stderr)
    sys.exit(1)



@API_bp.route('/')
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

            data = request.get_json()
            

            # Ensure data is a dictionary (not a list)
            if not isinstance(data, dict):
                return jsonify({"error": "Invalid data format, expected an object"}), 400

            key = generate_2fa_secret() 
            
            result = my_db.Create_Client(Data=data, twoFA_key_var=key)#Creates the user, return True id successful, False if not

            if not result:  
                return jsonify({"error": "User creation failed"}), 400  

            return jsonify({"2FA_key": key, "message": "User created successfully"}), 200  #Return the key to the user for connect the 2FA app

        except Exception as e:
            
            return jsonify({"error": str(e)}), 500  

    return jsonify({"error": "Invalid request method"}), 405
        
"""

import requests



r = requests.post(data={'name': 'Alice', 'age': 25}, url='http://127.0.0.1:1234/api/add_user')


if r.status_code == 200:
    print(r.text)
else:   
    print('Error:', r.status_code)

"""