from flask import Flask


def Create_App():
    app = Flask(__name__)
    
    #!When we use url_prefix, we are telling Flask to add the prefix to the URL of all the routes in the blueprint.
    
    from web.admin.routes import admin_bp #import the blueprint object
    app.register_blueprint(admin_bp,url_prefix='/admin') #register the blueprint object in the app
    
    from web.Main_page.routes import Main_page_bp #import the blueprint object
    app.register_blueprint(Main_page_bp,url_prefix='/') #register the blueprint object in the app
    
    from web.login_page.routes import login_bp #import the blueprint object
    app.register_blueprint(login_bp,url_prefix='/login') #register the blueprint object in the app
    
    return app