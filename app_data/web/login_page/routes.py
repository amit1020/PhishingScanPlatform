from flask import Blueprint, render_template




login_bp = Blueprint(
    'login_page', __name__, 
    template_folder='templates',
    static_folder='static',
    static_url_path='/login_page/static')




@login_bp.route('/')
def user_hello():
    return "Hello sadsadka"








