#!/usr/bin/env python3.10

app = Flask(__name__)

@app.route("/api")
def index():
	return render_template("index.html")

if __name__ == "__main__":
	app.run()
