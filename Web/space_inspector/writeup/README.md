> # Space Inspector
> > Web - 50pts
>
> The flag is lost in space, but if you inspect it closely you might find it.


## Writeup
The website looks empty, but if we use `inspect element` we can see that the flag is commented out at the bottom of the HTML.

```html
<body>
    <div class="main"></div>
    <!-- UiTHack24{insp3ct1ng_7h3_5p4c3_3l3men75!} -->
</body>
```