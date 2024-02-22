> # Space Station
> > Web - 493pts/8 solves
>
> The Spaceship Enigma is trying to locate the Stellar Nexus Alpha space station but are having troubles due to treacherous space dust in the area. The ship is receiving strange transmission which they think may be the final piece to locate the space station.

## Writeup
To solve the task, you need to decrypt the key before the rotors change which is every 20 seconds. Each rotor is a dictionary where each key and value are characters. For example, the encrypted key could be E* and rotor1 can have the following mapping {E: f,*: g } and rotor2 {f: 1, g: 2} and lastly rotor3 {1: h, 2: i} which results in the key being decrypted to hi. You must then make a post request to the server with the decrypted key according to the provided format to retrieve the flag.

```
UiTHack24{Wow_this_flag_is_way_to_long_to_find_manually_is_it_not_?}
```