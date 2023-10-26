#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>


int main(){
    // %7$s
    char *flag = "UiTHack24{some_flag_for_testing}";
    char buffer[40];
    fgets(buffer, 40, stdin);
    printf(buffer);

    return 0;
}