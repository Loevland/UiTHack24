#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char enc_flag[24] = {0x6c, 0x50, 0x6d, 0x71, 0x58, 0x5a, 0x52, 0x0b, 0x0d, 0x42, 0x4a, 0x08, 0x4d, 0x51, 0x66, 0x51, 0x09, 0x55, 0x56, 0x5a, 0x4b, 0x09, 0x57, 0x44};

void *enc1(char *str, int key){
    for(int i = 0; i < 24; i++){
        str[i] ^= key;
    }
}

int validate_key(char *input){
    enc1(input, 0x39);
    if(!memcmp(input, enc_flag, 24)){
        return 1;
    } else {
        return 0;
    }
}

int main(){
    char input[40] = {0};

    printf("Enter the key: ");
    fgets(input, 40, stdin);

    if(validate_key(input)){
        printf("Correct key!\n");
    } else {
        printf("Wrong key!\n");
    }
    return 0;
}
