> # Noob3
> > Noob - 147pts/48 solves
>
> Oh no! Someone deleted `flag.txt` from our system, and our spaceship is broken, so we are not able to go back in `history` to retrieve it.
>
> You can connect to the server with the following command: `nc uithack.td.org.uit.no 6002`
> The username is `noob3`
> The password is the flag from `noob2`

## Writeup
The commands we run on Linux are stored in a file called `.bash_history` for a while. If we run `cat .bash_history` we find the flag inside it. Alternatively the `history` command will also show the flag.

```
UiTHack24{1337_t1m3_tr4v3ll3r}
```