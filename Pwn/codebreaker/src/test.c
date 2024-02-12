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