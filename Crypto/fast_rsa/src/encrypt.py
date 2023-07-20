from Crypto.Util.number import bytes_to_long, getPrime

with open("flag.txt", "rb") as f:
    flag = f.read().strip()

m = bytes_to_long(flag)
p = getPrime(512)
q = getPrime(512)
n = p * q
e = 3

ct = pow(m, e, n)
print(f"{ct=}")
print(f"{n=}")
print(f"{e=}")