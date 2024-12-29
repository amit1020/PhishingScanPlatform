from flask import Flask


def Create_App():
    app = Flask(__name__)
    
    @app.route("/")
    def home():
        return "Hello, World!"
    
    from web.admin.routes import admin_bp #import the blueprint object
    app.register_blueprint(admin_bp) #register the blueprint object in the app
    
    from web.product.routes import product_bp #import the blueprint object
    app.register_blueprint(product_bp) #register the blueprint object in the app
    
    
    
    return app