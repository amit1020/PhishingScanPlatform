from flask import Blueprint, render_template



#Define the blueprint: 'product', set its url prefix: app.url/product
product_bp = Blueprint(
    'product', __name__,
    template_folder='templates',
    static_folder='static'
)







@product_bp.route('/')
def product_home():
    return render_template('product.html')
    