> # Yet Another Overflow
> > Pwn - 493pts/8 solves
>
> I came over this program which gives us a flag if we can guess the correct password. However, rumours say that it will take longer than the universe's lifetime to guess the password. Can you help me out?

## Writeup
This challenge is a `ret2win` challenge, where you can overflow the buffer and overwrite the return address on the stack with the address of the `success` function. The `success` function will print the flag for us.

Instead of writing the address of the `success` function directly after the offset, we must add a `ret` gadget before it, because of [the MOVAPS issue](https://ropemporium.com/guide.html#common-pitfalls).


Solve script can be found in [solve.py](./solve.py)