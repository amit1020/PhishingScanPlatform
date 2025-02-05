from flask import Flask
from .assets import register_sass_folders



def Create_App():
    app = Flask(__name__)
    
    
    #?app.config.from_object('config.Config') #!This line will import the Config class from the config.py file and load the configuration into the app object.
    
    #!When we use url_prefix, we are telling Flask to add the prefix to the URL of all the routes in the blueprint.
    from web.admin.routes import admin_bp #import the blueprint object
    app.register_blueprint(admin_bp,url_prefix='/admin') #register the blueprint object in the app
    
    from web.Main_page.routes import Main_page_bp #import the blueprint object
    app.register_blueprint(Main_page_bp,url_prefix='/') #register the blueprint object in the app
    
    from web.login_page.routes import login_bp #import the blueprint object
    app.register_blueprint(login_bp,url_prefix='/login') #register the blueprint object in the app
    
    from web.api.routes import API_bp #import the blueprint object
    app.register_blueprint(API_bp,url_prefix='/api') #register the blueprint object in the app
    
    #Handle errors(404), if the page was not found
    @app.errorhandler(404)
    def not_found_error(error):
        return "This page was not found", 404
    
    register_sass_folders(app)
    
    return app


#!Need  to make Config class in the config.py file, and import it here. check with ChatGPT: example:
"""
class Config:
    # סוד להגנה על פרטי הפעלה של טופס
    SECRET_KEY = 'your_secret_key_here'

    # הגדרות לפיתוח
    DEBUG = True

    # הגדרות מסד נתונים
    SQLALCHEMY_DATABASE_URI = 'sqlite:///your_database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # הגדרות שרת דוא"ל לשליחת הודעות
    MAIL_SERVER = 'smtp.yourserver.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'your-email@example.com'
    MAIL_PASSWORD = 'your-email-password'

    # נתיבי עבודה נוספים או הגדרות API
    # API_KEY = 'YOUR_API_KEY_HERE'


"""



"""
    


    # הגדרת מטפלי שגיאות
    @app.errorhandler(404)
    def not_found_error(error):
        return "This page was not found", 404

    # הגדרת Assets
    assets = Environment(app)
    sass_bundle = Bundle('src/sass/*.scss', filters='pyscss', output='dist/css/styles.css')
    assets.register('sass_all', sass_bundle)

    return app
    
"""