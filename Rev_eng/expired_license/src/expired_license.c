#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char enc_flag[24] = {0x15, 0x06, 0x09, 0x4b, 0x14, 0x18, 0x4b, 0x17, 0x24, 0x13, 0x0f, 0x13, 0x08, 0x4a, 0x4f, 0x00, 0x10, 0x49, 0x1a, 0x18, 0x2f, 0x33, 0x2e, 0x12};

void *enc3(char *str){
    for(int i = 0; i < 24; i += 2){
        char tmp = str[i];
        str[i] = str[i + 1];
        str[i + 1] = tmp;
    }
}

void *enc1(char *str, int key){
    for(int i = 0; i < 24; i++){
        str[i] ^= key;
    }
}

void *enc2(char *str){
    for(int i = 0; i < 12; i++){
        char tmp = str[i];
        str[i] = str[23 - i];
        str[23 - i] = tmp;
    }
}

int validate_key(char *input){
    enc1(input, 0x39);
    enc2(input);
    enc1(input, 0x42);
    enc3(input);

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