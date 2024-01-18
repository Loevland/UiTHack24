# WRITEUP 

If one hates themselves this can be solved mathematically since all the keys are in order.

The intended solution is to convert the pattern to regex and use a tool such as exrex to generate a word list.
The word list can then be scrolled through to find the correct entry/key.

example:

exrex '[c-m]\d[f-z]{2}[2-7][1-5]' -o wordlist.txt

sed -n '585937p' wordlist.txt