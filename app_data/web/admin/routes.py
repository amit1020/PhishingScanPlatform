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




admin_bp = Blueprint(
    'admin', __name__, 
    template_folder='templates',
    static_folder='static',
    static_url_path='/admin/static'
)







@admin_bp.route('/')
def product_home():
    return render_template('admin_home.html')



    
@admin_bp.route('/add_user', methods=['POST'])
def add_user(data):
    data = request.form
    print(data)
    pass


def Test():
    with Database_Class.Database_Connection_Class("a") as dbp: #*dbp is the object of Database_Connection_Class. dbp - Database Pointer 
        print(dbp.Get_Connection_Status())
        
    
    
    

if __name__ == '__main__':
    Test()
    