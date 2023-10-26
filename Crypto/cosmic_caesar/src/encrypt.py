def encrypt(text):
    flag_enc = ""
    for idx, char in enumerate(text):
        if char in alphabet:
            if idx % 2 == 0:
                flag_enc += alphabet[(alphabet.index(char)+3) % len(alphabet)]
            else:
                flag_enc += alphabet[(alphabet.index(char)-3) % len(alphabet)]
        else:
            flag_enc += char
    return flag_enc

def decrypt(text):
    flag_dec = ""
    for idx, char in enumerate(text):
        if char in alphabet:
            if idx % 2 == 0:
                flag_dec += alphabet[(alphabet.index(char)-3) % len(alphabet)]
            else:
                flag_dec += alphabet[(alphabet.index(char)+3) % len(alphabet)]
        else:
            flag_dec += char
    return flag_dec

alphabet = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

with open("flag.txt", "r") as f:
    flag = f.read().strip()

enc_flag = encrypt(flag)
print(enc_flag)
print(decrypt(enc_flag))
