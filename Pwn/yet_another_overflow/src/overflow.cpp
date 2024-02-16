#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>
#include "hash.h"

#define BUF_SIZE 16

constexpr uint64_t password = fnv1a<uint64_t>::hash("sduhpoqw");

void ignore_me(){
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

void timeout(int signal){
    if (signal == SIGALRM){
        printf("You timed out!\n");
        _exit(0);
    }
}

void ignore_me_timeout(){
    signal(SIGALRM, timeout);
    alarm(60);
}

void success() {
    FILE* f = fopen("flag.txt", "r");
    char flag[64];
    fgets(flag, 64, f);
    puts(flag);
    putchar('\n');
    fclose(f);
    exit(0);
}

void fail() {
    printf("Wrong password!\n");
}

int main() {
    ignore_me();
    ignore_me_timeout();

    char input[BUF_SIZE];

    printf("Enter password: ");
    scanf("%s", input);

    if (fnv1a<uint64_t>::hash(input) != password) {
        fail();
    } else {
        success();
    }
    return 0;
}