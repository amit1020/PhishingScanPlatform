from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import time
#This module converts binary data to Hexadecimal
from binascii import hexlify


"""
public_key:  meant for encryption

private_key:  meant for decryption   
    
"""


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



private,public = generate_key()
data = encrypt_message(public,"Hello World")
time.sleep(2)
Decrypt_(private,data)


