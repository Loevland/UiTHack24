> # Expired License
> > Rev - 430pts/22 solves
>
> The subscription on the software for our spaceship has expired, and we can't get back to Earth without it. We don't want to pay for a new license. Can you find the required license key by reversing the software?


## Writeup
The program asks for a key, so we have to reverse the program to find what the key is.

Loading the program in `IDA` we can see a `main` function that looks something like this.
```c
int main(){
  char input[40];
  printf("Enter the key: ");
  fgets(input, 40, stdin);
  if ( (unsigned int)validate_key(input) )
    puts("Correct key!");
  else
    puts("Wrong key!");
  return 0;
}
```

The `validate_key` function calls one function, and checks if out input is equal to what is stored in `enc_flag` (which is `6C 50 6D 71 58 5A 52 0B 0D 42 4A 08 4D 51 66 51 09 55 56 5A 4B 09 57 44`).
```c
int validate_key(const void *input){
  enc1(input, 57LL);
  return memcmp(input, &enc_flag, 0x18uLL) == 0;
}
```

### Enc1
```c
_BYTE *__fastcall enc1(__int64 a1, char a2){
  _BYTE *result; // rax
  int i; // [rsp+18h] [rbp-4h]
  for ( i = 0; i <= 23; ++i ){
    result = (_BYTE *)(i + a1);
    *result ^= a2;
  }
  return result;
}
```
This function XORs our input with 57.


To find out what the key the program asks for is, we need to XOR the bytes stored in `enc_flag` with 57. An example of this can be seen in [solve.py](./solve.py)

```
UiTHack24{s1th_h0locr0n}
```