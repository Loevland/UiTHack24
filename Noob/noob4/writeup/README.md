> # Noob - Noob4
> > Noob - 400pts
>
> Our trip through space and time seems to have messed with the future, and now we cannot access our flag!
>
> You can connect to the server with the following command: `nc uithack.td.org.uit.no 6003`
> The username is `noob4`
> The password is the flag from `noob3`

## Writeup
There is a file called `-flag.txt ` (with a space on the end). It is not possible to do as `noob1` and `cat -flag.txt ` to get the flag, because of the `-`.

The trick is to run `cat -- "-flag.txt "`, as this prevents the `-` in the filename from causing problems.

```
UiTHack24{d4sh_31337}
```