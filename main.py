from flask import Flask, url_for, render_template, request, redirect, session 
import sqlite3
from db_scripts import *
from random import shuffle

app = Flask(__name__)

def start_session(quiz_id = 0):
    session['quiz'] = quiz_id
    session['last_question'] = 0
    session['right_ans'] = 0
    session['total'] = 0

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        quizes = get_quizes()
        return render_template('start.html', quiz_list=quizes)
    else:
        quiz_id = request.form.get("quiz")
        print(quiz_id)
        start_session(quiz_id)
        return redirect(url_for('test'))


def save_answer():
    quiz_content_id = request.form.get('q_id')
    answer = request.form.get('ans_get')
    session['last_question'] = quiz_content_id
    session['totla'] += 1



def  quest_form(question):
    quest_list = [question[2], question[3], question[4], question[5]]
    shuffle(quest_list)
    return render_template('test.html', question=question[1],quest_id=question[0] ,answers_list=quest_list)


@app.route('/test', methods=["POST", "GET"])
def test():
    result = get_question_after(session['last_question'], session['quiz'])
    if not('quiz' in session or session['quiz'] < 0):
        return redirect(url_for('index'))
    else:
        if request.method == 'POST':
            save_answer()
        next_question = get_question_after(session['last_question'], session['quiz'])
        if next_question is None or len(next_question) == 0:
            return redirect(url_for('result'))
        else:
            return quest_form(next_question)
        # session['last_question'] = result[0]
        # return '<h1>' + str(session['quiz']) + '<br>' + str(result) + '</h1>'
    #return render_template('test.html')

@app.route('/result')
def result():
    return render_template('result.html')

app.config['SECRET_KEY'] = '12345678' 


@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(port=5000)