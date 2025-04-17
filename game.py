from flask import Flask, request, render_template

app = Flask(__name__)
response = ""
gameon = False

@app.route("/", methods=["GET", "POST"])
def index():
    global response, gameon

    if request.method == "POST":
        if "startgame" in request.form:
            word = request.form.get("user_input", "")
            response = start_game(word)
        elif "stopgame" in request.form:
            gameon = False
            response = "Spelet är avslutat."

    return render_template("index.html", response=response, gameon=gameon)

def start_game(word):
    global gameon
    gameon = True
    return f"Nu börjar vi. Ordet består av {len(word)} bokstäver. Tryck på avsluta om du vill sluta spela!"

if __name__ == "__main__":
    app.run(debug=True)