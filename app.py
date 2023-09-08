from boggle import Boggle
from flask import Flask, request, render_template, redirect, jsonify
from flask import session, make_response
from flask_debugtoolbar import DebugToolbarExtension


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
    session["score"] = 0
    session["guessed_words"] = []
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

    if word in session["guessed_words"]:
        result = "You already found this one!"
        return jsonify({"message": result, "score": session["score"]})

    result = boggle_game.check_valid_word(session["board"], word)

    if result == "ok":
        session["guessed_words"].append(word)

        if session["score"]:
            session["score"] += score_word(word)

        else:
            session["score"] = score_word(word)

    return jsonify({"message": result, "score": session["score"]})


def score_word(word):
    """Give guessed word a score based on number of characters"""
    return len(word)
