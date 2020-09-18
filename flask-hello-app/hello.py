import os
import pathlib

import flask
from dateutil.utils import today

this_file = pathlib.Path(__file__).resolve()
this_dir = this_file.parent.resolve()

os.chdir(this_dir)

app = flask.Flask(__name__)
app.secret_key = "very-secret-key-1234"


@app.route("/hello", methods=["GET"])
def handle_hello():
    context = {}
    if flask.session:
        age = int(flask.session.get("age", 0))
        year = today().year - age
        context.update(
            {
                "age": age,
                "name": flask.session.get("name"),
                "year": year,
            }
        )
    return flask.render_template("hello.html", **context)


@app.route("/hello-update", methods=["POST"])
def handle_hello_update():
    name = flask.request.form.get("name")
    age = flask.request.form.get("age")

    flask.session.update(
        {
            "name": name,
            "age": age,
        }
    )

    return flask.redirect("/hello")


@app.route("/hello-reset", methods=["POST"])
def handle_hello_reset():
    flask.session.clear()

    return flask.redirect("/hello")
