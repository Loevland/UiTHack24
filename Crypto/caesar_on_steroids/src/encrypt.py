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

with open("flag.txt", "r") as f:
    flag = f.read().strip()
alphabet = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
print(f"{encrypt(flag)}")
