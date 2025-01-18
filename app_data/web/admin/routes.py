from flask import Blueprint, render_template




admin_bp = Blueprint(
    'admin', __name__, 
    template_folder='templates',
    static_folder='static',
    static_url_path='/admin/static'
)







@admin_bp.route('/')
def product_home():
    return render_template('admin_home.html')
    


