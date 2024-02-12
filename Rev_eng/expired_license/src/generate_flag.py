flag = "UiTHack24{s1th_h0locr0n}"

def xor(s, key):
    return "".join([chr(ord(char) ^ key) for char in s])

flag = xor(flag, 0x39)

print("{", end="")
for idx, char in enumerate(flag):
    if idx != len(flag) - 1:
        print(f"0x{ord(char):02x}, ", end="")
    else:
        print(f"0x{ord(char):02x}", end="")

print("}")