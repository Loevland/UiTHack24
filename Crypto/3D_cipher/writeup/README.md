> # 3D Cipher
> > Crypto - 500pts/1 solve
>
> While I was navigating through Earth's space debris on my way to the moon, I came across a fascinating discovery - a Rubik's cube floating alongside a computer. My curiosity piqued, I decided to inspect the computer, unveiling not only an encryption algorithm, but also some encrypted text! I need your help to decipher it.

## Writeup

The flag can be thought of as being a solved rubik's cube and encrypted by scrambling the cube. To decrypt the flag, the moves used to scramble the cube must be performed in the reverse order. The rotatable Rubik's cube in the web browser represents the scrambled cube position. Any order of moves solving this cube will give a valid decryption key.

The right orientation of the cube must be used when solving the cube. The right orientation of the cube is shown when disabling rotation of the cube and refreshing the page. 

Putting the cube in an online solver: 
https://rubiks-cube-solver.com/solution.php?cube=0262412214363634416133144544631555351526623526231562514

A reverse rotation is the same as rotation the same side 3 times. The solving moves can be represented in the code as:

```c
L(2);F(2);B(1);D(3);B(3);R(1);F(2);B(2);R(3);U(3);F(1);R(1);U(1);R(2);B(2);D(3);B(2);R(2);U(3);
```

Or by changing the rotation functions to take in an unsigned int variable instead of int, the solving moves can be represented as:

```c
L(2);F(2);B(1);D(-1);B(-1);R(1);F(2);B(2);R(-1);U(-1);F(1);R(1);U(1);R(2);B(2);D(-1);B(2);R(2);U(-1);
```

Printing the cube will now show the flag.

\
**TLDR**:

```c
int main(){
    init();
    L(2);F(2);B(1);D(3);B(3);R(1);F(2);B(2);R(3);U(3);F(1);R(1);U(1);R(2);B(2);D(3);B(2);R(2);U(3);
    print_cube();
    
    return 0;
}
```