from flask import Flask, request, render_template, jsonify, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret'
app.debug = True
toolbar = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False




@app.route('/')
def main_route():
    return render_template('base.html', survey=satisfaction_survey)

@app.route('/agreement', methods=["GET","POST"])
def agree_route():
    session["responses"] = []
    return render_template('question_begin.html', survey=satisfaction_survey)


@app.route('/questions/<int:number>', methods=["GET", "POST"])
def get_question(number):
   
    if (len(session['responses']) != number):
        flash("Invalid Question")
        return redirect(f"/questions/{len(session['responses'])}")

    return render_template('question.html', num=number, survey=satisfaction_survey)

@app.route('/answer', methods=['POST'])
def handle_answer():
    answer = request.form['answer']
    ses = session['responses']
    ses.append(answer)
    session['responses'] = ses

    if (len(session['responses']) == len(satisfaction_survey.questions)):
        return redirect("/completed")
    else:
        return redirect(f"/questions/{len(session['responses'])}")


@app.route('/completed')
def completed():
    session.clear()
    return render_template('complete.html')