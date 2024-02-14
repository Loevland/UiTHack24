> # The great escape
> > Pwn - 400pts
>
> You have reached the dashboard of a ship, and you're ready to get away. However,
> the activation of the ship requires a password.<br/>
> You must find the password to activate the ship do your great escape!

## Writeup
To get the flag we have to guess a random 32 byte password, which is not feasible.

The program gives us the following options when ran:
1. Create guess: We are asked to specify the size of our guess, and then to input our guess into a malloced chunk
2. Delete guess: Our guess is freed, and the guess zeroed out
3. View guess: Our guess is printed to the screen
4. Generate password: 32 random bytes are read in, creating the password we have to guess
5. Guess password: If our guess is equal to the password we get the flag, otherwise not


The vulnerability in the program is when it deletes our guess. When the guess is deleted, the actual pointer to the heap address is not zeroed out, creating a `Use-After-Free` vulnerability which we can use to `view` the contents of that heap chunk.

However, the password and our guess are two different pointer variables, so how does this help us?

The libc-version on Ubuntu 22 (which is used, look in the Dockerfile) uses the `tcache` as a caching mechanism when chunks are freed. Chunks of similar sizes that are freed are put into the same `bin`, and then reused for later `malloc` calls of the same size. Because of the UAF vulnerability, we can see the contents of the `guess` chunk, even after it is freed, and because of the `tcache` we are able to view the password by doing the following operations:
- Create a guess with size `0x20` (less also works because of tcache minimum size)
- Delete the chunk (so that it is put in the `tcache`, but we still have the pointer to it an can view the contents of it)
- Generate password (this will reuse our `guess-chunk` to put the password in)
- View guess (because our `guess-chunk` is now also pointing to the location where the password is stored, so we can just read it!)

Now that we have the password (it is in bytes, so most of it will not be ascii characters) we can create a new guess (which will be our actual guess), and put in the password which we know is correct.

For full exploit script see [solve.py](./solve.py)

```
UiTHack24{h1pp17y_h0ppi7y_y0u_g0t_off_th3_pr0p3r7y}
```
