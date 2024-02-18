> # Noob5
> > Noob - 326pts/34 solves
>
> Get the flag to join the galactic elite!
>
> You can connect to the server with the following command: `nc uithack.td.org.uit.no 6004`
> The username is `noob5`
> The password is the flag from `noob4`

## Writeup
With `ls -al` we can see that the `flag.txt` file is no readable by us (noob5), only `root` and `elite`. The user `elite` has a home directory in `/home/elite`, which contains a file, `cat`. This file has the setuid bit set, which means that we can execute the file as if we were the `elite` user.

We can therefore get the flag by running `./cat ../noob5/flag.txt` from the `/home/elite` directory.

```
UiTHack24{7h3_n00b_g4l4ct1c_31337}
```