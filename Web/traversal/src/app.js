const express = require("express");
const fs = require("fs");
const path = require("path");
const app = express();
const port = 9001;

app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "static/index.html"));
});

app.get("/static", (req, res) => {
  try {
    var page = path.join(__dirname, "static/", req.query.page);
  } catch (err) {
    res.status(404).send("Invalid request");
    return;
  }
  fs.stat(page, (err, _) => {
    if(err == null){
      res.sendFile(page);
    } else {
      res.status(404).send("Page does not exist");
    }
  });
});

app.post("/login", (req, res) => {
  res.send("Login is currently disabled");
});

app.listen(port, () => {
  console.log(`Listening at port: ${port}`);
});
