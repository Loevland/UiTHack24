> # Xenithian doorway
> > Pwn - 499pts/4 solves
>
> Inside the book you retrieved from the archived you find a map which leads to the exit. After following the map you reach a door marked as the exit. The door seems locked, but with the correct passphrase, and the slight malfunction of the door you can try to escape!


## Writeup
The binary reads input with `scanf("%s", passphrase);`, which is vulnerable to a buffer overflow, because `scanf` with `%s` reads all the characters we write in.

The binary is also compiled without `NX`, which lets us execute shellcode from the stack.
```console
$ checksec ./doorway
    Arch:     amd64-64-little
    RELRO:    Full RELRO
    Stack:    No canary found
    NX:       NX unknown - GNU_STACK missing
    PIE:      PIE enabled
    Stack:    Executable
```

Running the program also prints to us the address of the input buffer on the stack, `printf("Error code: %p\n", passphrase);`. The combination of the 3 things mentioned allows us to:
- Input assembly code which executes a shell on the server
- Overwrite the return address with the address of `passphrase`, which is printed to us when running the program. This makes the execution of the program jump to our input, which will give is shell

See [exploit.py](./exploit.py) for full exploit script

```
UiTHack24{Op3nS3z4m3}
```