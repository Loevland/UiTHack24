enc_flag = "6C 50 6D 71 58 5A 52 0B 0D 42 4A 08 4D 51 66 51 09 55 56 5A 4B 09 57 44".split(" ")
enc_flag = [int(x, 16) for x in enc_flag]

flag = ""
for x in enc_flag:
    flag += chr(x ^ 57)
print(flag)