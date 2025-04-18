from flask import Flask, request, render_template

app = Flask(__name__)
response = ""
gameon = False
under_line = ""
word = ""
word_list = []
guesses = []
number_of_guesses = 7
stage = 0
hangman_stages = [
        """
       ------
            |
            |
            |
            |
            |
    =========
    """,
    """
       ------
       |    |
            |
            |
            |
            |
    =========
    """,
    """
       ------
       |    |
       O    |
            |
            |
            |
    =========
    """,
    """
       ------
       |    |
       O    |
       |    |
            |
            |
    =========
    """,
    """
       ------
       |    |
       O    |
      /|    |
            |
            |
    =========
    """,
    """
       ------
       |    |
       O    |
      /|\\   |
            |
            |
    =========
    """,
    """
       ------
       |    |
       O    |
      /|\\   |
      /     |
            |
    =========
    """,
    """
       ------
       |    |
       O    |
      /|\\   |
      / \\   |
            |
    =========
    """
]

@app.route("/", methods=["GET", "POST"])
def index():
    global response, gameon, under_line, word, word_list, guesses, stage

    if request.method == "POST":
        if "startgame" in request.form:
            if gameon:
                response = "Spelet är redan igång"
            else:
                stop_game()
                word = request.form.get("user_input", "")
                word_list = list(word)
                response = start_game(word)
                
        elif "stopgame" in request.form:
            stop_game()
        elif "guess" in request.form:
            if not gameon:
                response = "Du måste starta spelet först!"
            else:
                guess = request.form.get("user_input", "")
                handle_guess(guess)

    return render_template("index.html", response=response, guesses=guesses, gameon=gameon, hangman_stages=hangman_stages[stage], under_line=under_line)

def start_game(word):
    global gameon, under_line
    if len(word) < 1:
        return "Skriv in ordet som du vill starta med"
    gameon = True
    for w in range(0, len(word)):
        under_line += "_"
    answer = (f"Nu börjar vi. Du har {number_of_guesses} chanser att gissa fel.\n" 
              f"Ordet består av {len(word)} bokstäver.\n"  
              f"Skriv in en bokstav och tryck Gissa! Tryck på avsluta om du vill sluta spela!")
    return answer

def handle_guess(guess):
    global word_list, under_line, response, stage, gameon
    index = 0
    correct_guess = False
    guesses.append(guess)
    
    if len(guess) == 1:
        for l in word_list:
            
            if l == guess:
                #rätt gissning, lägg in bokstaven i under_line
                under_line = under_line[0:index] + l + under_line[index+1: len(word)]
                response = "Rätt gissat!"
                correct_guess = True
            index += 1
        if not correct_guess:
            
            response = "Tyvärr " + guess + " var inte rätt. Försök igen"
            if stage > 6:
                gameon = False
                response = "Game over!"
            else:
                stage += 1
            
        if under_line == word:
            response = "Du vann! Det rätta ordet var: " + word
            gameon = False
    else:
        if guess == word:
            response = "Du vann! Det rätta ordet var: " + word
            gameon = False
        else:
            response = guess + " var inte rätt ord, försök igen!"
            stage += 1

def stop_game():
    global response, gameon, under_line, word, word_list, guesses, stage
    gameon = False
    response = "Spelet är avslutat."
    word = ""
    under_line = ""
    word = ""
    guesses = []
    word_list = []
    stage = 0        


if __name__ == "__main__":
    app.run(debug=True)