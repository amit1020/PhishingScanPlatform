from flask import (
    Blueprint, render_template, request,jsonify
)


import sys, os,json



sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../Functions_and_Classes')))

try:
    import Database_Class, TwoFA_functions #Properly imported
    my_db = Database_Class.Database_Connection_Class('lt')
    
except ImportError as e:
    print(f"Error importing Database_Class: {e}", file=sys.stderr)
    sys.exit(1)




#Define the blueprint: 'product', set its url prefix: app.url/product
API_bp = Blueprint('API_bp', __name__)






@API_bp.route('/')
def product_home():
    return "hello world"
    
    
@API_bp.route('/add_user/', methods=['POST'])
def add_user():
    if request.method == 'POST':
        try:
            data = request.get_json()
            """_data consist of:
                    - name
                    - email
                    - password
                    - phone
            """
            key = TwoFA_functions.generate_2fa_secret()
            # Check if data is received as a list
            if isinstance(data, list) and len(data) > 0:
                user_data = data[0]  # Extract the first dictionary from the list
            else:
                return jsonify({"error": "Invalid data format"}), 400
                

            result = my_db.Create_Client(Data=user_data,twoFA_key_var=key)#Save the process of creating the user - can be True/False
            if not result: #If the user was not created
                return 404         
             
            #TODO - Check if the data is valied and if the user was added to the database 
            return json.dumps(key)

            #convert to json
            return json.dumps("Success")
        except Exception as e:
            print(str(e))
            return 404
        
        
        
        
        
"""

import requests



r = requests.post(data={'name': 'Alice', 'age': 25}, url='http://127.0.0.1:1234/api/add_user')


if r.status_code == 200:
    print(r.text)
else:   
    print('Error:', r.status_code)

"""