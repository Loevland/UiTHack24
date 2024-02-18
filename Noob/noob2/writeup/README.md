> # Noob2
> > Noob - 132pts/49 solves
>
> Our flag was stolen once again. This time we think they have `hidden` it. Can you get it back for us?
>
> You can connect to the server with the following command: `nc uithack.td.org.uit.no 6001`
> The username is `noob2`
> The password is the flag you found in `noob1`
>
> Read up on the `ls` command to get the flag

## Writeup
We do not see anything special if we run `ls`, because the flag file is `hidden`. Hidden directories and files can be seen with the command `ls -al`. With this command we find a directory `.secret`, which has the `flag.txt` file inside it.

```
UiTHack24{7h3r3_1s_n0_h1ding_fr0m_7h3_1337_0f_3m_4ll}
```