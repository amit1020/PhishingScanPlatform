from flask import Flask


def Create_App():
    app = Flask(__name__)
    
    
    from web.admin.routes import admin_bp #import the blueprint object
    app.register_blueprint(admin_bp) #register the blueprint object in the app
    
    from web.Main_page.routes import Main_page_bp #import the blueprint object
    app.register_blueprint(Main_page_bp,url_prefix='/') #register the blueprint object in the app
    
    
    
    return app