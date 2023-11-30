#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define USERNAME "noob4"
#define PASSWORD "UiTHack24{1337_t1m3_tr4v3ll3r}"
#define USERLEN 5
#define PASSLEN 30


void ignore_me(){
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

int main(){
    ignore_me();

    char user[USERLEN+1];
    char pass[PASSLEN+1];

    printf("Username: ");
    scanf("%5s", user);

    printf("Password: ");
    scanf("%30s", pass);

    if(strncmp(user, USERNAME, USERLEN) == 0 && strncmp(pass, PASSWORD, PASSLEN) == 0){
        puts("Logged in! Use 'exit' to logout");
        puts("Here is your shell!\n");
        system("ls");
        system("/bin/sh");
    } else {
        puts("Invalid Username or Password!");
    }
    return 0;
}