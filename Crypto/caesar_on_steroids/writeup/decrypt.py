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
    flag_enc = f.read().strip()
alphabet = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
print(decrypt(flag_enc))
