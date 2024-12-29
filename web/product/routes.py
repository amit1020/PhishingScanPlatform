from flask import Blueprint, render_template




product_bp = Blueprint(
    'product', __name__,
    template_folder='templates',
    static_folder='static'
)







@product_bp.route('/product')
def product_home():
    return "Hello product"