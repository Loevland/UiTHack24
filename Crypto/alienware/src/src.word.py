"""
    ORIGINAL FILE: do not distribute during the competition
    Encryptinator 9000
    Crypto: medium
    UiTHack 2024
    FLAG: UiTHack24{E.T._ph0ne_h0me_plsss}
"""

import sys, os
import random

KEY = "S3cr3tK3y"  # replaced with "s3CR3Tk3Y"
KEY_SWAPPED = KEY.swapcase()


def encrypt_data_easy(data: bytes) -> bytes:
    random.seed(8008135)  # replaced with "NiceTry"
    for i in range(len(data := bytearray(data))):
        data[i] ^= cryptinator()
    return bytes(data)


def cryptinator() -> int:
    return (((~(random.randint(0, 255))) << 2) ^ 0b10101010) & 0b01010101


def encrypt_data_medium(data: bytes) -> bytes:
    random.seed(8008135)  # replaced with "NiceTry"
    for i in range(len(data := bytearray(data))):
        data[i] ^= cryptinator() ^ cryptinator_v2(i) ^ KEY.encode("utf-8")[i % len(KEY)]
    return bytes(data)


def cryptinator_v2(x: int) -> int:
    return (((((~(random.randint(0, 4096)))) & 0b10101010) ^ x) | 0b01010101) % 256


if __name__ == "word.py":
    if sys.argv[1] != "encrypt":
        print(
            "SAFEGUARD: All files in the directory will be encrypted. Run with argument 'encrypt' if you accept."
        )
        print("Example: python3 word.py encrypt")
        exit()

    # find files to encrypt in cwd
    for filename in os.listdir("."):
        # skip encryptinator.py
        if filename == sys.argv[0]:
            continue
        # skip already encrypted files
        if filename.endswith(".enc"):
            continue
        with open(filename, "wb") as f:
            content = f.read()
            f.write(encrypt_data_medium(content))
            os.rename(filename, filename + ".enc")
    # remove seed and change key value
    with open(__name__, "w") as f:
        f.write(f.read().replace("8008135", '"NiceTry"').replace(KEY, KEY.swapcase()))
    # delete this file
    os.remove(__name__)


## not provided in the challenge ##

"""
    Can be decrypted by running a second time, since it only uses xor
"""


def encrypt_data_medium_swapped(data: bytes) -> bytes:
    random.seed(8008135)
    for i in range(len(data := bytearray(data))):
        data[i] ^= cryptinator() ^ cryptinator_v2(i) ^ KEY.swapcase().encode("utf-8")[i % len(KEY)]
    return bytes(data)


if __name__ == "__main__":

    match sys.argv[1]:
        case "assert":
            # test cryptinator and decryptinator
            test_str = b"Testing some reallly hard to crack  \r encryption"
            assert encrypt_data_easy(encrypt_data_easy(test_str)) == test_str
            assert encrypt_data_medium(encrypt_data_medium(test_str)) == test_str
            h = b"hello world!"
            print(
                a := encrypt_data_medium(h), encrypt_data_medium(a), encrypt_data_medium_swapped(a)
            )
            # check that decryption can not be reversed with swapped key
            assert encrypt_data_medium_swapped(encrypt_data_medium(h)) != h

        case "encrypt":
            # used to create src material
            # encrypt file
            with open(sys.argv[2], "rb") as f:
                content = f.read()
            with open(sys.argv[2] + ".enc", "wb") as f:
                f.write(encrypt_data_medium(content))

        case "decrypt":
            # decrypt file
            with open(sys.argv[2], "rb") as f:
                content = f.read()
            with open(sys.argv[2] + ".dec", "wb") as f:
                f.write(encrypt_data_medium(content))
