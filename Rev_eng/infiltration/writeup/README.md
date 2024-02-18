> # Infiltration
> > Rev - 490pts/9 solves
>
> You are given a covert mission to infiltrate an enigmatic alien base located within the depths of Dexius. Accomplishing this mission will demand your utmost courage and skills, as you're set to engage in a fierce space battle against aliens.

## Writeup

The APK file given can be unpacked like a normal zip file. Inside the unapcked folder, there is a file called `classes`. Using the `file` command on it shows `classes: Dalvik dex file version 038`. Dalvik dex files are normally ended with the extension ".dex". Many online decompiler will not be able to decompile the dex file without the file extension. Therefore, renaming `classes`to `classes.dex` and decompiling it with https://www.decompiler.com/ will give the source code of the APK file inside `sources/com/uithack/spaceinvaders`. 

Here there is a `Flag.java` file. The flag can be printed by running the code after changing it to:

```java
public class Flag {
    public static char[] str = {'x', 'D', 'y', 'e', 'L', 'N', 'F', 31, 25, 'V', 'z', 'E', 30, '_', 30, 'r', 28, 24, 'r', '@', 'T', 'r', 'N', 'X', ']', 'r', 29, 'K', 'r', 'G', 25, '[', 25, 18, 'P'};

    public static void main(String[] args) {
        for (int i = 0; i < 35; i++) {
            System.out.print((char)(str[i] ^ '-'));
        }
    }
}
```