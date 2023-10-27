from Crypto.Util.number import long_to_bytes
from gmpy2 import iroot

with open("out.txt", "r") as f:
    ct = int(f.readline().strip().split("=")[1])
    n = int(f.readline().strip().split("=")[1])
    e = int(f.readline().strip().split("=")[1])

m = iroot(ct, e)[0]
print(long_to_bytes(m).decode())
