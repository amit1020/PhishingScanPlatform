import configparser, pyotp,time,qrcode,PIL
from pathlib import Path


#TODO improve the secuirity
def read_ini_file(action,api_name) -> configparser.SectionProxy:
    if action == "api" and api_name != None: #Check if the action is to get the api key
        config = configparser.ConfigParser()
        
        config.read(Path(__file__).parent.parent / "config.ini" ) #get the path of the config file
        
        if "api" in api_name and api_name in config.sections(): #Check if the api name is in the config file
            return config['APIs'] #return the api key
        else:
            return None
        
    elif action == "Database_Connection" and api_name == None:
        config = configparser.ConfigParser()
        config.read(Path(__file__).parent.parent / "config.ini" )#found the path of the config file
        return config['mysql_database_for_connection']
        
        
    else:
        return None
    
        
# Generate a 2FA secret
def generate_2fa_secret():
    totp = pyotp.TOTP(pyotp.random_base32())
    return totp.secret #! This is the secret key that be stored in the database





def Create_QR(key:str,name:str) -> bool:
    if key == None or name == None:
        return False
    try:
        uri = pyotp.totp.TOTP(key).provisioning_uri(name=name, 
                                                issuer_name="Phishing_Scan_Platform")#create the uri - URL identification of the 2FA 
        
        QRC = qrcode.make(uri).save(f"{name}.png") #Create the QR code and save it to the file
        return True
    except Exception as e:
        print(e)#!Remove this line
        return False
    
    
    
#Vertify the OTP
def verify_otp(secret_key, otp):
    print(otp)
    
    return pyotp.TOTP(secret_key).verify(otp,valid_window=0) #! This is the secret key that be stored in the database








if __name__ == "__main__":
    key = generate_2fa_secret()
    Create_QR(key,"test")


  









"""  2FA example code 

    from flask import Flask, request, session
    import pyotp

    app = Flask(__name__)
    app.secret_key = 'your_secret_key_here'

    # יצירת מפתח סודי (במקרה האמיתי יש לאחסן בבסיס נתונים)
    secret = pyotp.random_base32()

    @app.route('/')
    def index():
        if 'otp' in session:
            return 'Logged in using 2FA!'
        return 'You are not logged in'

    @app.route('/login', methods=['POST'])
    def login():
        user_otp = request.form['otp']
        if pyotp.TOTP(secret).verify(user_otp):
            session['otp'] = True
            return 'You are logged in'
        return 'Login failed'

    if __name__ == '__main__':
        app.run(debug=True)
        
"""


