> # Cosmic Caesar
> > Crypto - 50pts
>
> While traveling through the debris of exploded planets, a signal arrived. We've determined the alien alphabet used, but the message is still encrypted. Your mission is to decrypt the secret message.

## Writeup
The name of the challenge hints to a `Caesar cipher`, and if we look at `encrypt.py` we can see that every odd-index character is shifted to the right 3 times, and every even-index character is shifted to the left 3 times.

To solve the challenge we decrypt the caesar cipher by rotating the characters back, as in [solve.py](./solve.py), where we only change the + and - of the encrypt function.

```
UiTHack24{1nt3rg4lact1c_ca3s4r}
```