from flask import Flask, jsonify, request
import random
from apscheduler.schedulers.background import BackgroundScheduler
from cryptography.fernet import Fernet
import base64

app = Flask(__name__)
scheduler = BackgroundScheduler()
scheduler.start()

rotor1 = {} 
rotor2 = {}
rotor3 = {}

characters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 
                'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 
                'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y',
                'Z', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', '0',
                '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '<', '=', '>', '?', '@', '[',
                ']', '^', '_', '`', '{', '|', '}', '~']

flag = None

encryption_key = None
use_this = None
encrypted_content = None

def generate_flag(): 

    tmp_encryption_key = generate_key()

    with open("flag.txt", 'r') as file:
        content = file.read()
        print(f"Secret key before: {content}")
    global encrypted_content
    encrypted_content = encrypt(content, tmp_encryption_key)
    print(f"Encrypted content: {encrypted_content}")
    characters_shuffled1 = characters.copy()
    random.shuffle(characters_shuffled1)
    rotor1.clear()
    idx = 0
    for character in characters: 
        rotor1[character] = characters_shuffled1[idx]
        idx += 1

    characters_shuffled2 = characters.copy()
    random.shuffle(characters_shuffled2)
    rotor2.clear()
    idx = 0
    for character in characters: 
        rotor2[character] = characters_shuffled2[idx]
        idx += 1

    characters_shuffled3 = characters.copy()
    random.shuffle(characters_shuffled3)
    rotor3.clear()
    idx = 0
    for character in characters: 
        rotor3[character] = characters_shuffled3[idx]
        idx += 1

    print(f"Encryption_key Original: {tmp_encryption_key}")
    content_rotor3 = ''
    for character in tmp_encryption_key: 
        for key, value in rotor3.items(): 
            if value == character: 
                content_rotor3 += key
    print(f"Encryption_key after rotor3: {content_rotor3}")

    content_rotor2 = ''
    for character in content_rotor3: 
        for key, value in rotor2.items(): 
            if value == character: 
                content_rotor2 += key
    print(f"Encryption_key after rotor2: {content_rotor2}")

    content_rotor1 = ''
    for character in content_rotor2: 
        for key, value in rotor1.items(): 
            if value == character: 
                content_rotor1 += key
    print(f"Encryption_key after rotor1: {content_rotor1}")

    global encryption_key
    encryption_key = content_rotor1

    decrypt_test()

scheduler.add_job(generate_flag, trigger='interval', seconds=20)

def decrypt_test(): 
    
    tmp = encryption_key

    tmp1 = ''
    tmp2 = ''
    tmp3 = ''

    for character in tmp: 
        for key, value in rotor1.items(): 
            if character == key: 
                tmp1 += value
    for character in tmp1: 
        for key, value in rotor2.items(): 
            if character == key: 
                tmp2 += value
    for character in tmp2: 
        for key, value in rotor3.items(): 
            if character == key: 
                tmp3 += value

    flag = decrypt(encrypted_content, tmp3)

    print(f"Secret key after: {flag}")

def generate_key():
    key = Fernet.generate_key()
    return base64.urlsafe_b64encode(key).decode()

def encrypt(word, key):
    if not isinstance(word, str):
        raise ValueError("Input must be a string")
    
    cipher_suite = Fernet(base64.urlsafe_b64decode(key.encode()))
    encrypted_word = cipher_suite.encrypt(word.encode())
    return base64.urlsafe_b64encode(encrypted_word).decode()

def decrypt(encrypted_word, key):
    if not isinstance(encrypted_word, str):
        raise ValueError("Input must be a string")
    
    cipher_suite = Fernet(base64.urlsafe_b64decode(key.encode()))
    encrypted_bytes = base64.urlsafe_b64decode(encrypted_word)
    decrypted_word = cipher_suite.decrypt(encrypted_bytes).decode()
    return decrypted_word

@app.route('/get_encrypted')
def get_encrypted(): 
    response = [encryption_key]
    return jsonify(response)

@app.route('/get_rotors')
def get_rotor(): 
    response = [{"rotor1": rotor1,
                 "rotor2": rotor2,
                 "rotor3": rotor3}]
    return jsonify(response)

@app.route('/post_decrypt', methods=['POST'])
def post_decrypt(): 
    data = request.get_json()
    if 'key' in data: 
        decrypt_key = data['key']
        try: 
            secret_flag = decrypt(encrypted_content, decrypt_key)
            response_message = f"{secret_flag}"
        except: 
            response_message = "Error: Invalid key"
    else:
        response_message = "Error: 'key' is missing in the provided JSON data."

    response_data = {'response': response_message}
    return jsonify(response_data)

if __name__ == '__main__': 
    generate_flag()
    app.run(host="0.0.0.0", debug=True, port=8009)
