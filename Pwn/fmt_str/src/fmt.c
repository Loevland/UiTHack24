#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <signal.h>

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

int main(){
    ignore_me();
    ignore_me_timeout();

    char flag[64];
    char buffer[20];

    FILE *f = fopen("flag.txt", "r");
    if (f == NULL){
        printf("Flag File is Missing, contact Admin\n");
        return 0;
    }
    fgets(flag, 64, f);
    fclose(f);

    puts("Write something here!");
    fgets(buffer, 21, stdin);
    printf(buffer);

    return 0;
}