> # Noob1
> > Noob - 116pts/50 solves
>
> Our flag was stolen from our spaceship, and we need your 1337 hacker skills to get it back for us.
>
> You can connect to the server with the following command: `nc uithack.td.org.uit.no 6000`
> The username is `noob1`
> The password is `noob1.
>
> Read up on the `cat` command to get the flag

## Writeup
When we log in we have a shell on the server. There is a file `flag.txt` in the directory, which we can get by typing `cat flag.txt`.

```
UiTHack24{7h3_1337357_0f_3m_4ll}
```