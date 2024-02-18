enc_flag = "3c3d1c29020859064f115e4242471011434147686e046a3e0f316b585d540b3133585a09124153544e7d"
enc_flag = [enc_flag[i:i+2] for i in range(0, len(enc_flag), 2)]
enc_flag = bytes([int(x, 16) for x in enc_flag])
enc_flag = enc_flag[::-1]

flag = ""
prev = ""
for idx, x in enumerate(enc_flag):
    if idx == 0:
        prev = x
        flag = chr(x) + flag
    else:
        flag = chr(x ^ prev) + flag
        prev = ord(flag[0])

print(flag)
