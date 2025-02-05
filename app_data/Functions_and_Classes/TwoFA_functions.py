import pyotp,time,qrcode,PIL



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