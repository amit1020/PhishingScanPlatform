from flask import (
    Blueprint, render_template, request 
)
import sys, os



sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../Functions_and_Classes')))

try:
    import Database_Class #Properly imported
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
            name = request.form['name']
            age = request.form['age']
            return "Success"
        except Exception as e:
            print(str(e))
            return "Failed" 
        
    