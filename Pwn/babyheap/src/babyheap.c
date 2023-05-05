#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <signal.h>
#include <unistd.h>
#include <sys/random.h>


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

void menu(){
    puts("1. Create Guess");
    puts("2. Delete guess");
    puts("3. View guess");
    puts("4. Generate password");
    puts("5. Guess password");
    puts("6. Exit");
    printf(">> ");
}

char *create_guess(int *guess_set){
    char *guess = malloc(0x20);
    printf("Enter your guess:\n>> ");
    fgets(guess, 0x21, stdin);
    *guess_set = 1;
    puts("Guess created!\n");
    return guess;
}

void delete_guess(char **guess, int *guess_set){
    if (*guess != NULL)
        free(*guess);
    *guess_set = 0;
    puts("Guess deleted!\n");
}

void view_guess(char *guess){
    if (guess != NULL){
        puts("Your guess is:");
        puts(guess);
    }
    else{
        puts("No guess created!\n");
    }
}

char *generate_password(){
    char *password = malloc(0x20);
    getrandom(password, 0x20, 0);
    for(int i = 0; i < 0x20; i++){
        if(password[i] == '\0' || password[i] == '\n')
            password[i] = '\x41';
    }
    puts("Password generated!\n");
    return password;
}

void guess_password(char *guess, char *password, int guess_set){
    if(guess == NULL || password == NULL || guess_set == 0){
        puts("You need to create a guess and generate a password first!\n");
        return;
    }
    if(!strncmp(guess, password, 0x20)){
        puts("Correct password, here is your flag!");
        print_flag();
        exit(0);
    }
    else {
        puts("Wrong password!\n");
    }
}


/*
    1. Create Guess
    2. Delete guess
    3. View guess
    4. Generate password
    5. Guess password
    6. Exit
*/
int main(){
    ignore_me();
    ignore_me_timeout();

    int input, guess_set = 0;
    char *password = NULL, *guess = NULL;

    while(1){
        menu();
        if (scanf("%d%*c", &input) == 0)
            exit(0);
        switch (input){
            case 1:
                guess = create_guess(&guess_set);
                break;
            case 2:
                delete_guess(&guess, &guess_set);
                break;
            case 3:
                view_guess(guess);
                break;
            case 4:
                password = generate_password();
                break;
            case 5:
                guess_password(guess, password, guess_set);
                break;
            case 6:
                exit(0);
            default:
                puts("Invalid option!\n");
                break;
        }
    }
    return 0;
}