import random
from argon2 import PasswordHasher

if False:
    d = bytearray("hunter2", "utf-8")
    c = bytearray("*" * len(d), "utf-8")
    e = bytearray(range(len(d)))
    print(d == b"hunter2")
    a = b"hunter2"
    for i in range(len(a)):
        pass
        b = d[i] ^ c[i]
        c[i] = (d[i] | e[i]) ^ c[i]
        print(b)
    print(c, c == b"B_D]O]\x1c")
    print(c == b"\66\95\68")

ph = PasswordHasher()
res = ph.hash("hunter2")
res2 = ph.hash("AzureDiamondCthon98")
print(res)
print(res2)
with open("pswd.txt", "w") as f:
    f.write(res2)


def verify_admin(pswd: str):
    if len(pswd) == 0:
        return False

    p = bytearray(pswd, "utf-8")
    x = bytearray("*" * len(pswd), "utf-8")
    for i in range(len(pswd)):
        x[i] = (p[i] ^ i) ^ x[i]

    return x == b"B^F]K]\x1e"


print(verify_admin("hunter2"))
