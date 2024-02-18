> # Alienware
> > Crypto - 499pts/4 solves
>
> Aliens have encrypted my very important file! Luckily they forgot to delete the software from the trash folder, can you help me decrypt it?

## Writeup

The encryption algorithm uses a simple XOR cipher. The key is staticly declared in the file, however this has tampered with. A nonce is also use which is seeded with a specific number. The seed is removed from the seed function, but it is revealed by the replace function in main. The real key value can also be deciphered from the operations done to the real key.

```py
# remove seed and change key value
with open(filename, "wb") as f:
    f.write(f.read().replace(b"8008135", b"NiceTry").replace(KEY, KEY.swapcase()))
```

We then have the seed value of 8008135, which can be inserted in all the seed functions.
The real key value is not explicitly written like the seed. However reversing the _swapcase_ method can be done by applying it again.

Solution:

```py
random.seed("NiceTry") -> random.seed(8008135)
KEY = "s3CR3Tk3Y" -> KEY = "S3cr3tK3y"

# decrypt a file
with open(sys.argv[1], "rb") as f:
        content = f.read()
with open(sys.argv[1] + ".dec", "wb") as f:
    f.write(encrypt_data(content))
```

After these changes the file can be decrypted by applying the same encryption algorithm again.
The amazing gpt generated [space novel](../src/Stardust-reckoning.txt) can then be enjoyed, and halfway through our friend E.T. reveals the flag.

Flag:

```txt
UiTHack24{E.T._ph0ne_h0me_plsss}
```
