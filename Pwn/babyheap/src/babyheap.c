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

int get_int(){
    int input;
    printf(">> ");
    scanf("%d%*c", &input);
    return input;
}

void menu(){
    puts("1. Create guess");
    puts("2. Delete guess");
    puts("3. View guess");
    puts("4. Generate password");
    puts("5. Guess password");
    puts("6. Exit");
}

char *create_guess(){
    printf("Enter guess size:\n");
    int size = get_int()+1;
    if(size <= 0 || size > 0xff){
        puts("Invalid size!\n");
        return NULL;
    }
    char *guess = malloc(size);
    printf("Enter guess:\n>> ");
    fgets(guess, size, stdin);
    printf("Guess created!\n");
    return guess;
}

void delete_guess(char *guess){
    free(guess);
    guess = NULL;
    printf("Guess deleted!\n");
}

void view_guess(char *guess){
    printf("Your guess is:\n%s\n", guess);
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

void guess_password(char *guess, char *password, int guessed){
    if(guess == NULL || password == NULL || guessed == 0){
        puts("You need to create a guess and generate a password first!\n");
        return;
    }
    if(!memcmp(guess, password, sizeof(password))){
        puts("Correct password!");
        print_flag();
    } else {
        puts("Wrong password!\n");
    }
}

int main(){
    ignore_me();
    ignore_me_timeout();

    int input;
    char *guess = NULL;
    int guessed = 0;
    char *password = NULL;

    while(1){
        menu();
        input = get_int();
        switch (input){
            case 1:
                guess = create_guess();
                guessed = 1;
                break;
            case 2:
                delete_guess(guess);
                guessed = 0;
                break;
            case 3:
                view_guess(guess);
                break;
            case 4:
                password = generate_password();
                break;
            case 5:
                guess_password(guess, password, guessed);
                break;
            case 6:
                exit(0);
            default:
                puts("Invalid option!\n");
                return 0;
        }
    }
    return 0;
}