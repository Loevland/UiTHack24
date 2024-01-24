import os, time
import flask
from flask_sock import Sock
from simple_websocket.ws import ConnectionClosed

from argon2 import PasswordHasher
import json, uuid
import random, secrets
import logging
from logging import DEBUG
from json import JSONDecodeError


app = flask.Flask("placeholder")
app.secret_key = secrets.token_bytes(32)
sock = Sock(app)


@app.route("/", defaults={"path": "index.html"})
@app.route("/<path:path>")
def static_files(path: str):
    print("requesting", path)
    if path == "index.html":
        return flask.render_template("index.html", name=path)
    elif path == "flag.txt":
        return flask.make_response("No flag for you :P")
    elif path.startswith("log/"):
        path = path.split("/")[-1]
        return flask.send_from_directory("log", path)
    return flask.send_from_directory("static", path)
    return flask.render_template("index.html", name=path, items=None)


def verify_admin(pswd: str) -> bool:
    p = bytearray(pswd, "utf-8")
    x = bytearray("*" * len(pswd), "utf-8")
    for i in range(len(pswd)):
        x[i] = (p[i] | i) ^ x[i]

    return x == b"B_D]O]\x1c"


def verify_knowledge(pswd: str) -> bool:
    ph = PasswordHasher()
    with open("pswd.txt", "r") as f:
        return ph.verify(f.read(), pswd)
    return False


START_COINS = 200
SPIN_COST = 20
PAYOUT_MULTIPLIER = 5
FLAG_PRICE = 10000
LOG_KEEP_TIME = 60 * 5  # value in seconds
WS_TIMEOUT = 60 * 5  # value in seconds


@sock.route("/ws")
def connect(ws):
    addr = repr(ws.sock).split("=")[-1][:-1]
    session_id = uuid.uuid4()
    session = {
        "secret": app.secret_key,
        "id": session_id.__str__(),
        "addr": addr,
        "coins": START_COINS,
    }

    app.logger.info(f"New WS connection from {addr}")

    # add a session log file to logging handler
    handler = logging.FileHandler(f"log/{session['id']}.log")
    app.logger.addHandler(handler)
    app.logger.info(f"New connection from {addr}")

    while True:
        try:
            body = ws.receive(timeout=WS_TIMEOUT)
            if body is None:
                app.logger.info(f"Session timed out: {session['id']}, after {WS_TIMEOUT}s")
                break
            msg = json.loads(body)

            method = msg["type"]
            if method == "info":
                ws.send(
                    json.dumps(
                        {
                            "type": "info",
                            "session_id": session["id"],
                            "coins": session["coins"],
                            "spin_cost": SPIN_COST,
                            "flag_price": FLAG_PRICE,
                            "win_payout": SPIN_COST * PAYOUT_MULTIPLIER,
                        }
                    )
                )
            elif method == "spin":
                if session["coins"] >= SPIN_COST:
                    session["coins"] -= SPIN_COST
                    roll = [random.randint(0, 9) for i in range(3)]
                    if roll[0] == roll[1] == roll[2]:
                        session["coins"] += SPIN_COST * PAYOUT_MULTIPLIER
                        ws.send(
                            json.dumps(
                                {
                                    "type": "spin",
                                    "coins": session["coins"],
                                    "roll": roll,
                                    "prize": SPIN_COST * 5,
                                    "win": True,
                                }
                            )
                        )
                    else:
                        ws.send(
                            json.dumps(
                                {
                                    "type": "spin",
                                    "coins": session["coins"],
                                    "roll": roll,
                                    "win": False,
                                }
                            )
                        )
                else:
                    ws.send(
                        json.dumps(
                            {
                                "type": "error",
                                "message": "You are broke, come back when you got some more money.\nYou need more than 20 coins to spin!",
                            }
                        )
                    )

            elif method == "flag":
                if session["coins"] >= FLAG_PRICE:
                    session["coins"] -= FLAG_PRICE
                    ws.send(json.dumps({"type": "flag", "flag": open("/flag.txt").read()}))
                    app.logger.info(f"Someone got the flag! {addr=}, {msg=}")
                elif session["admin"] == True:
                    session["flag"] = open("flag.txt").read()
                else:
                    ws.send(
                        json.dumps(
                            {
                                "type": "error",
                                "message": "You need more than 1 million coins to get the flag!",
                            }
                        )
                    )

            # admin api
            elif method == "login":
                if verify_admin(msg["password"]):
                    session["admin"] = True
                    ws.send(json.dumps({"type": "admin", "message": "Logged in"}))
            elif method == "logout":
                session.pop("admin")
                ws.send(json.dumps({"type": "admin", "message": "Logged out"}))
            elif method == "debug":
                if session.get("admin", False):
                    app.logger.setLevel(DEBUG)
                    ws.send(json.dumps({"type": "admin", "message": "Debug mode enabled"}))
            elif method == "motherload":
                if session.get("admin", False) and verify_knowledge(msg["password"]):
                    session["coins"] += FLAG_PRICE * 100
                    ws.send(
                        json.dumps(
                            {
                                "type": "admin",
                                "message": "Motherload activated!",
                                "coins": session["coins"],
                            }
                        )
                    )

        except ConnectionClosed:
            break
        except JSONDecodeError or TypeError:
            app.logger.error(f"Invalid JSON from {addr}")
            ws.send(json.dumps({"type": "error", "message": "Invalid JSON"}))
        except Exception as e:
            app.logger.error(f"Error from {addr}:", e)
            # if the flag is added to the session dict, this will leak it
            app.logger.debug("Session terminated: ", session)
            ws.send(
                json.dumps(
                    {"type": "error", "message": "Don't be mean, the server got feelings 2 ;/"}
                )
            )
    # remove session log file from logging handler
    app.logger.removeHandler(handler)
    # clean up old session logs
    # remove all logs older than LOG_KEEP_TIME seconds
    for f in os.listdir("log"):
        if time.time() - os.path.getmtime(f"log/{f}.log") > LOG_KEEP_TIME:
            os.remove(f"log/{f}")

    ws.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
