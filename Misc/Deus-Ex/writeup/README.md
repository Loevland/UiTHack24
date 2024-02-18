> # Deus Ex
> > Misc - 500pts/2 solves
>
> Hey it's me, JC.
> I've heard you could use some help, so I whipped up something special just for you.
> Make you sure you go to the right place. Oh, and you will also need a 4-digit code for the padlock.
> Don't worry, If you know me you probably already know the code.
> If not, you'll just have to learn to immerse yourself in the simulation.

## Writeup
To find the flag is not only hidden inside the image, it is also encrypted with a 4-digit code using this website:
[https://www.pelock.com/products/steganography-online-codec](https://www.pelock.com/products/steganography-online-codec)
The encryption used by the website, PBKDF2, is written on the image.
Searching for "steganography PBKDF2" should give the above website as the first online tool.

The code 0451 is a running joke in the immersive sim genre. If the hacker is aware of this, it should be clear that 0451 is the code they "already know".
If not, searching for "Immersive sim code" will give 0451 as the first result on Google.

Alternatively searching for "Deus Ex code", resulting wiki sites mention 0451 as the code to the first locked door in several Deus Ex games. 0451 is also highlighted blue, linking to a wiki page for this number.

1.  Goto [https://www.pelock.com/products/steganography-online-codec](https://www.pelock.com/products/steganography-online-codec)
2. Upload provided image
3. Provide "0451" as the password
4. The image should decode to: `UiTHack24{d3nt0n-in-7he-machin3}`