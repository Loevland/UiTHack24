> # Archive
> > Pwn - 200pts
>
> Having escaped the Xenithians, you now stand before a cryptic Xenithian archive. <br/>
> Retrieve the book of secrets from the archive!

## Writeup
If we look at the source code we see that the flag is read into a buffer on the stack. Later `printf(buffer)` is called. This line contains a *format string* vulnerability, where we are able to print values stored on the stack (which is where the flag is located!).

If we enter the input `%X$p` (where X is a number indicating the position of the stack we are reading values from) we are able to get out hex values from the stack. By trial and error we will eventually find hex values which looks like ascii at position 12, 13, and 14, when our input is `%12$p %13$p %13$p`. The output is then `�0x326b636148546955 0x345f617833687b34 0x345f617833687b34`.

If we convert these hex values to ascii, and reverse the order of the ascii representation, we get the flag.

```
UiTHack24{h3xa_4rch1ves}
```
