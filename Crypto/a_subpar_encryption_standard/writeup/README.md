> # A subpar encryption standard
> > Crypto - 481pts/12 solves
>
> While looking around in the remains of an enemy spaceship you find some code.
> In their hurry they must have forgotten that there were more steps to do.
> Your priority is to decrypt the code to maybe find some indication of who the ship belonged to.

## Writeup
The encrypted text is in hexadecimal.

To decrypt the text one has to do the byte sub step from decryption of AES using the inverse Rijndael S-box.

After that one simply converts from hexadecimal back to ascii characters.