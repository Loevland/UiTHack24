#include <stdio.h>
#include <signal.h>
#include <unistd.h>

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

    char passphrase[60] = {0};
    printf("Error code: %p\n", passphrase);
    printf("Passphrase:\n> ");
    scanf("%s", passphrase);
    return 0;
}