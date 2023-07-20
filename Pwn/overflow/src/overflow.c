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

void print_flag(){
    char chr;
    FILE *f = fopen("flag.txt", "r");
    chr = fgetc(f);
    while (chr != EOF){
        printf("%c", chr);
        chr = fgetc(f);
    }
    printf("\n");
    fclose(f);
}

void vuln(){
    char secret[10] = "P4ssw0rd!";
    char input[10];

    printf("Give me some input:\n");
    fgets(input, 0x20, stdin);

    if(strncmp(secret, "Flag_plzz!", 10) == 0){
        puts("Here is your flag:");
        print_flag();
    } else {
        printf("\nSorry, secret is not correct\n");
        printf("Input: %s", input);
        printf("Secret: %s\n", secret);
    }
}

int main(){
    ignore_me();
    ignore_me_timeout();

    vuln();

    return 0;
}