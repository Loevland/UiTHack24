"""
    Encryptinator 9000
    Crypto: easy, medium
    UiTHack 2024
"""

KEY = "s3CR3Tk3Y"

import sys, os
import random


def cryptinator() -> int:
    return ((((~(random.randint(0, 255))) << 2) ^ 0b10101010) & 0b01010101)

def cryptinator_v2(x:int) -> int:
    return (((((~(random.randint(0, 4096)))) & 0b10101010) ^ x) | 0b01010101) % 256

def encrypt_data(data:bytes) -> bytes:
    random.seed("NiceTry")
    for i in range(len(data := bytearray(data))):
        data[i] ^= cryptinator() ^ cryptinator_v2(i) ^ KEY.encode("utf-8")[i % len(KEY)]
    return bytes(data)


if __name__ == "__main__":
    if sys.argv[1] != "encrypt":
        print("SAFEGUARD: All files in the directory will be encrypted. Run with argument 'encrypt' if you accept.")
        print("Example: python3 word.py encrypt")
        exit()

    for n in os.listdir("."):
        if n == sys.argv[0]:
            continue
        if n.endswith() == ".enc":
            continue
        with open(n, "wb") as f:
            c = f.read()
            f.write(encrypt_data(c))
            os.rename(n, n + ".enc")
        with open(n, "wb") as f:
            f.write(f.read().replace(b"8008135", b"NiceTry").replace(KEY, KEY.swapcase()))
        os.remove(__name__)