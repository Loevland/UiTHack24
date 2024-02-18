> # Rapid Encryption
> > Crypto - 392pts/27 solves
>
> Those pesky aliens keep sniffing our messages and stealing our supplies! Luckily I have come up with a way to encrypt our messages so that they won't know where our supplies are located. I had to improve the encryption time of the algorithm, but I'm sure it makes no difference...

## Writeup
This is a RSA challenge, where the primes `p` and `q` are 512 bits in size, so we will not be able to guess them. However, `e` is 3, but usually it is 65537. Because `e` is so small, the ciphertext `ct` might not be large enough when `ct^e` is calculated such that the modulus `N` is utilized.

This means that we can just find the cube root of the ciphertext to get the flag. See [decrypt.py](./decrypt.py) for the python solution.

```
UiTHack24{3ncryp7i0n_g0es_brrrr}
```