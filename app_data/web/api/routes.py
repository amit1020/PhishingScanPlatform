from flask import (
    Blueprint, render_template, request,url_for,jsonify
)
import sys, os,json,base64,io
from PIL import Image



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






@API_bp.route('/auth/', methods=['POST'])
def auth():
    pass
    
    
    
    
    
    
    
@API_bp.route('/add_user/', methods=['POST'])
def add_user():
    if request.method == 'POST':
        try:
            #Make roles for the data 
            data = request.get_json()
            """_data consist of:
                    - name
                    - email
                    - password
                    - phone
            """
            #!Check if the data is valid
            if my_db.Create_Client(Data=data):
                #* If the user was created successfully and the QR was created successfully 
                return json.dumps("Success")
                
            else:
                return json.dumps("Error")      
                    
            #convert to json
            
        except Exception as e:
            print(str(e))
            return json.dumps("Error")
        
        
        
        
        
"""

import requests



r = requests.post(data={'name': 'Alice', 'age': 25}, url='http://127.0.0.1:1234/api/add_user')


if r.status_code == 200:
    print(r.text)
else:   
    print('Error:', r.status_code)

"""