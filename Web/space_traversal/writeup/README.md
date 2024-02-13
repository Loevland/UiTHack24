> # Space traversal
> > Web - 250pts
>
> In the search for a new planet to inhabit, we have found a couple different candidates.<br/>
> I have collected images of them, so that you can help me decide which one to go to.


## Writeup
The website contains some images. If we click at one of the images we see the URL change to `https://uithack.td.org.uit.no:8001/images/?image=crystallara.jpg`.

Looking at the source code we can see that if we click an image we hit the `/images` endpoint, which first removes any `../` in the url (to "prevent" path traversal), then sets the image path for the image we clicked for (in this case `crystallara.jpg`), then the file is sent back to us if it exists.
```js
app.get("/images", (req, res) => {
  try {
    // No path traversal
    var image = req.query.image.replace(/\.\.\//g, "");
    var image_path = path.join(__dirname, "static/images/", image);
  } catch (err) {
    console.log(err);
    res.status(404).send("Invalid request");
    return;
  }

  fs.stat(image_path, (err, _) => {
    if(err == null){
      res.sendFile(image_path);
    } else {
      res.status(404).send(image_path + " does not exist");
    }
  });
});
```

While this code checks for path traversal with `../`, it does not prevent path traversals, which allows us to read the flag.

The code checks for `../` and remove it if it exists, but what happens if we send `....//`? Then the first `../` is removed, but because it is replaced with nothing, the URL still contains `../` (because only the "inner" `../` is removed)
If we change the `?image=...` to `?image=....//....//flag.txt` we get the flag, as the "filtration" makes the URL `?image=../../flag.txt`.

```
UiTHack24{n0t_th3_tr4v3rse_1_w45_3xp3c71ng}
```