"""
    Alienware solve
    Crypto: medium
    UiTHack 2024
"""

# swap the key to original
KEY = "s3CR3Tk3Y".swapcase()

import sys, os
import random


def abcd() -> int:
    return (((~(random.randint(0, 255))) << 2) ^ 0b10101010) & 0b01010101


def efgh(x: int) -> int:
    return (((((~(random.randint(0, 4096)))) & 0b10101010) ^ x) | 0b01010101) % 256


def scrambleinator(x: bytes) -> bytes:
    # insert the correct seed
    random.seed(8008135)
    for i in range(len(x := bytearray(x))):
        x[i] ^= abcd() ^ efgh(i) ^ KEY.encode("utf-8")[i % len(KEY)]
    return bytes(x)


if __name__ == "__main__":
    for n in os.listdir("."):
        if n == sys.argv[0]:
            continue
        if n.endswith(".enc"):
            with open(n, "rb") as f:
                c = f.read()
                with open(n + ".dec", "wb") as f:
                    f.write(scrambleinator(c))
