alphabet = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
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

with open("flag.txt.enc", "r") as f:
    enc_flag = f.read()

print(decrypt(enc_flag))