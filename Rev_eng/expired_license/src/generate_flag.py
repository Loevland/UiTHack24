flag = "UiTHack24{s1th_h0locr0n}"

def reverse(s):
    return s[::-1]

def xor(s, key):
    return "".join([chr(ord(char) ^ key) for char in s])

def swap_pairs(s):
    # Swap index 0 with 1, 2 with 3, etc.
    return "".join([s[idx + 1] + s[idx] for idx in range(0, len(s), 2)])

flag = xor(flag, 0x39)
flag = reverse(flag)
flag = xor(flag, 0x42)
flag = swap_pairs(flag)

print(flag)
print("{", end="")
for idx, char in enumerate(flag):
    if idx != len(flag) - 1:
        print(f"0x{ord(char):02x}, ", end="")
    else:
        print(f"0x{ord(char):02x}", end="")

print("}")