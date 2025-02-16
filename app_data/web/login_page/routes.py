from flask import Blueprint, render_template, redirect, url_for, request, flash, session







login_bp = Blueprint(
    'login_page', __name__, 
    template_folder='templates',
    static_folder='static',
    static_url_path='/login_page/static')




@login_bp.route('/', methods=['GET'])
def PageShowUp():
    return render_template('/login.html') 







@login_bp.route('/test', methods=['GET'])
def product_home():
    return render_template('/user.html') 
    