#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv){
    if(argc != 2){
        printf("Usage: %s <seed>\n", argv[0]);
        return 0;
    }
    srand(atoi(argv[1]));
    for(int i = 0; i < 4; i++){
        rand();
    }
    int nums[3] = {rand()%34, rand()%34, rand()%34};
    printf("%d %d %d\n", nums[0], nums[1], nums[2]);
    return 0;
}