# Web - One armed bandit

> > Web - 300pts
>
>
> Files: [Source code](../src/app.py)
>

## Writeup

The challenge can be solved in three different intended ways:

- [The lucky](#the-lucky)
- [The hacker](#the-hacker)
- [The loremaster](#the-loremaster)

### The lucky

Getting the flag through sheer luck is possible according to the law of big numbers. However, the chances beating the challenge this way is very low. Definetely so within the timeslot of the ctf.

### The hacker

The most likely way to solve the challenge. The solution requires several steps to be performed in order:

- Reversing the admin password
- Logging in as admin
- Adding the flag to the session dictionary
- Use the admin api to enable debug mode
- Create an exception so that the session dict is written to the log
- Access the log through the url.

### The loremaster

This is a easter egg for the truly knowledgable about the early days of the internet. However even then it is not a trivial task to get the flag. By using the very obvious motherload api, the player can get an immense amount of money. This is mainly intended as a timesink, but nevertheless a intended and valid way to get the flag.
However there is and additional password protecting the api, along with the need of admin credentials. In contrast to the admin password which is easily reversed. It is not provided in the source file, and with the addition of beeing hashed with argon2. Which *hopefully* should make it impossible to brute force, [or other unintended ways](https://xkcd.com/538/).
By first reversing the admin password, many will recognise the admin password "hunter2" as a reference to a well known [irc conversation](https://knowyourmeme.com/memes/hunter2).
The password for the motherload api is a reference to the same conversation, and therefore beeing possible but still hard to guess. The password is `AzureDiamondCthon98` and was initially used as a testing feature, but was left/*intentionally forgotten*.

Flag:

```txt
UiTHack23{Passw0rd_1s_*******}
```
