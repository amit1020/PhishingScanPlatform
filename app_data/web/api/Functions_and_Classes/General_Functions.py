import configparser, pyotp,time,qrcode,PIL, bcrypt
from pathlib import Path


#Encryption and Decryption modules
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import time
#This module converts binary data to Hexadecimal
from binascii import hexlify







def HashPassword(pass_:str):
    _ = pass_.encode('utf-8')  # Convert password to bytes
    hashed = bcrypt.hashpw( _ , bcrypt.gensalt())
    return hashed



def VertifyPassword(pass_:str,hashed_pass:str):
    _ = pass_.encode('utf-8')  # Convert password to bytes
    return bcrypt.checkpw(_, hashed_pass)



def generate_key():
    PrivateKey = RSA.generate(2048) #Generate an RSA key of length 2048 bits
    PublicKey = PrivateKey.publickey() #Extract the public key from the private key
    with open("./Public.pem", "wb") as file: #Open a file to write the private key
        file.write(PublicKey.export_key())
    return PrivateKey,PublicKey



def encrypt_message(public_key,message:str):
    message = message.encode("utf-8") #Convert the message to bytes
    cipher_rsa = PKCS1_OAEP.new(public_key) #Create a new PKCS1_OAEP object with the public key
    
    encrypted_data = cipher_rsa.encrypt(message) #Encrypt the message
    print(f"Encrypted: {hexlify(encrypted_data)}") #Print the encrypted message
    
    return encrypted_data
    
    
    
    
def Decrypt_(private_key,encrypted_data):
    cipher_rsa = PKCS1_OAEP.new(private_key) #Create a new PKCS1_OAEP object with the private key
    decrypted_data = cipher_rsa.decrypt(encrypted_data) #Decrypt the message
    print(f"Decrypted: {decrypted_data.decode('utf-8')}") #Print the decrypted message








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


