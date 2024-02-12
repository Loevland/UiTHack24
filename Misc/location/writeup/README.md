> # Location
> > Misc - 100pts
>
> The aliens have captured three of our crew members and is holding them hostage at different locations. Luckily, they managed to send us pictures of their surroundings. Can you figure out where they are being held captive?
>
> The flag is the cities where these picture was taken, in lowercase, wrapped in UiTHack24{}. If you encouter any acute accent characters (e.g. à) in the city name, replace them with their non-accented counterparts (e.g. a).
>
> Example: UiTHack24{city1_city2_city3}

## Writeup
### City 1
The first image shows a skijump. On the left of the image we can see the olympic rings, indicating that the Olympic Games have been hosted at this location. At the right side of the image we can see an O. Oslo is the only city starting with an O which have held the Olympic Games in skijumping. The first city is therefore `oslo`.

### City 2
On the right side of the image we can see a large sign of the number 7 with the text `JÄRVEVANA B`. If we google Järvevana 7B we get a hit for the city of `Tallinn`. The second city is therefore `tallinn`.

### City 3
If we reverse image search the flower shoe in the image we will get a hit for `partizanske`.

The full flag is:
```
UiTHack24{oslo_tallinn_partizanske}
```