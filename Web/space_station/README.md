# Space Station
> Web - ???pts

The Spaceship Enigma is trying to locate the Stellar Nexus Alpha space station but are 
having troubles due to treacherous space dust in the area. The ship is receiving strange 
transmission which they think may be the final piece to locate the space station. 

## GET /get_encrypted
```
[
  "cSku;D'E,W18I2.$/pJp{b>RX7pAp!21JSReW7Ju<7~LYSBd{2.pJ8*X,N1-"
]
```

## GET /get_rotors
```
[
  {
    "rotor1": {
      "!": "f",
      "1": "A",
      "\"": ...,
    },
    "rotor2": {
     ...: ...,
    },
    "rotor3": {
     ...: ...,
    }
  }
]
```

## POST /post_decrypt
*body*
```
'key': 'bVZoSE00c2Z4NFlRMTEyYkoxV0I5a016S3c3dHFBcXk1NzFqZ1RlWUJDYz0='
```

```
{
    "response": "Error: Invalid key"
}
```

```
{
    "response":"Error: 'key' is missing in the provided JSON data."
}
```

```
{
  "response": "UiTHack2024{...}"
}
```
