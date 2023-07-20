#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <unistd.h>
#include <time.h>

void ignore_me(){
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

void timeout(int signal){
    if (signal == SIGALRM)
    {
        printf("You timed out!\n");
        _exit(0);
    }
}

void ignore_me_timeout(){
    signal(SIGALRM, timeout);
    alarm(60);
}

void banner(){
    printf("\n#       ####### ####### ####### ####### ######  #     #\n");
    printf("#       #     #    #       #    #       #     #  #   #\n");
    printf("#       #     #    #       #    #       #     #   # # \n");
    printf("#       #     #    #       #    #####   ######     #  \n");
    printf("#       #     #    #       #    #       #   #      #  \n");
    printf("#       #     #    #       #    #       #    #     #  \n");
    printf("####### #######    #       #    ####### #     #    #  \n\n");
}

void print_flag(){
    char chr;
    FILE *f = fopen("flag.txt", "r");
    chr = fgetc(f);
    while (chr != EOF){
        printf("%c", chr);
        chr = fgetc(f);
    }
    fclose(f);
}

void lottery(){
    int guesses[3] = {0};
    printf("Guess the 3 next numbers to win a prize!\n");
    printf("The first 4 numbers are:\n%d %d %d %d\n", rand()%34, rand()%34, rand()%34, rand()%34);

    printf("Your guess: ");
    scanf("%d %d %d", &guesses[0], &guesses[1], &guesses[2]);

    int winning_numbers[3] = {rand()%34, rand()%34, rand()%34};
    if(guesses[0] == winning_numbers[0] &&
       guesses[1] == winning_numbers[1] &&
       guesses[2] == winning_numbers[2]){
        printf("Congratulations, you win!\n");
        print_flag();
    } else {
        printf("The winning numbers were: %d %d %d\n", winning_numbers[0], winning_numbers[1], winning_numbers[2]);
        printf("Better luck next time!\n");
    }
}

int main(){
    ignore_me();
    ignore_me_timeout();

    unsigned long clock = time(NULL);
    char choice;
    banner();
    printf("Welcome to the PRNG!\n");
    printf("The current time is: %lu\n", clock);
    printf("Would you like to try your luck? (y/n): ");
    scanf("%c", &choice);

    if(choice == 'y' || choice == 'Y'){
        srand(clock);
        lottery();
    } else {
        printf("Goodbye!\n");
    }
    return 0;
}