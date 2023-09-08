from boggle import Boggle
from flask import Flask, request, render_template, redirect, jsonify
from flask import session, make_response
from flask_debugtoolbar import DebugToolbarExtension
from functions import is_word_in_file

app = Flask(__name__)

app.config['SECRET_KEY'] = "secretkey"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

boggle_game = Boggle()
words = boggle_game.words


@app.route("/")
def boggle_begin():
    """Clear Session Board and Generate New Boggle Board"""

    session["board"] = []
    session["board"] = boggle_game.make_board()

    return redirect("/boggle")


@app.route("/boggle")
def boggle_main():
    """Main page where Boggle is played"""

    board = session["board"]

    return render_template("boggle.html", board=board)


@app.route("/validate", methods=["GET"])
def check_word():
    """Check if word is valid"""

    word = request.args.get("word")
    result = boggle_game.check_valid_word(session["board"], word)

    return jsonify({"message": result})
