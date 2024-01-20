
def decrypt(encrypted_text, key):
    key = key * (len(encrypted_text) // len(key)) + key[:len(encrypted_text) % len(key)]
    decrypted_text = ""
    for char, key_char in zip(encrypted_text, key):
        decrypted_char = chr(ord(char) ^ ord(key_char))
        decrypted_text += decrypted_char
    return decrypted_text

if __name__ == "__main__":

    key = input("Enter key: ")
    with open("flag.txt", "r") as f: 
       encrypted_flag = f.read()
    flag = decrypt(encrypted_flag, key)
    print(flag)