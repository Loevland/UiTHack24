> # Codebreaker
> > Pwn - 100pts
>
> After saving the crew you've been captured by the Xenithians, and your escape depends on predicting the next three numbers of their code which changes each attempt. Luckily, the Xenithians seem to have left out a crucial vulnerability when generating their code. Crack the code to be set free!


## Writeup
Looking at the source code we see that the goal of this challenge if to guess the next 3 lottery numbers to get the flag. The lottery numbers are randomly generated, and seeded with the current time
```c
unsigned long clock = time(NULL);
srand(clock);
```

The time is printed to us, so we know the seed, and can therefore also predict the next 3 letters of the sequence. This little C program will generate the 4 numbers we are presented, and the last 3 numbers we have to guess. We just run the proram with the argument `<time>` to get the last numbers.
```c
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main(int argc, char **argv){
    if(argc != 2){
        printf("Usage: %s <time>", argv[0]);
        return -1;
    }
    srand(atoi(argv[1]));
    for(int i = 0; i < 7; i++){
        printf("%d\n", rand()%34);
    }
    return 0;
}
```

```
UiTHack24{X3n1th14n_3sc4p3}
```
