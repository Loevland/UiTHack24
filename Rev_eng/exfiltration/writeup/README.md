> # Exfiltration
> > Rev - 200pts
>
> Congratulations, Agent! You've successfully infiltrated the enigmatic alien base and managed to steal their highly classified code. However, it seems that it is written in some weird foreign language. Your next mission is to find out what the code does!


## Writeup
The javascript file asks us for the password when run, but the source code for it looks horrible!

To find the password that the program checks for we have to clean up the obfuscated program, and rename the variables and functions used. Most of the cleanup can be done using `ctrl+f` and `console.log` variable names and outputs. There are also a lot of unused strings in the initial program.

After some cleanup the code will look like [encrypt.js](./encrypt.js).

The password the program checks against is hex characters. The password check calculates the XOR of the first and second character, then the second and third character, etc. The last character is unencrypted, and is a `}`, so to decrypt it we can XOR the last character with the second last, second last with third last, etc.

A decryption script can be found in [solve.js](./solve.js)

```
UiTHack24{j4v4scr1p7_15_an_4l1en_l4ngu4g3}
```