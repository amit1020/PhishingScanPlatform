import pyotp,time,qrcode,PIL

from pathlib import Path #This module provides an object-oriented interface for working with filesystem paths
 



# Generate a 2FA secret
def generate_2fa_secret():
    totp = pyotp.TOTP(pyotp.random_base32())
    return totp.secret #! This is the secret key that be stored in the database





def Create_QR(key:str,user_name:str) -> bool:
    """_summary_

    Args:
        key (str): user_key
        user_name (str): user_name

    Returns:
        bool: _description_
    """
    if key == None or user_name == None:
        return False
    try:
        uri = pyotp.totp.TOTP(key).provisioning_uri(name=user_name, 
                                                issuer_name="Phishing_Scan_Platform")#create the uri - URL identification of the 2FA 
        
        QRC = qrcode.make(uri).save(Path(__file__).parent.parent / f"web/login_page/static/QR_image/{user_name}.png") #Create the QR code and save it to the file
        return True
    
    except Exception as e:
        print(e)#!Remove this line
        return False
    
    
    
#Vertify the OTP
def verify_otp(secret_key, otp):
    totp = pyotp.TOTP(secret_key) #Create TOTP object
    return totp.verify(otp) 







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