from flask import Flask, render_template, request
from pyquiz.game import mechanics
from pyquiz.data.setup_db import get_database_connection

app = Flask(__name__)

db_conn = get_database_connection(db_path=r"C:\Users\andyc\AppData\Local\Temp\pyquiz.db")



# get initial data
question = mechanics.get_current_question(db_conn=db_conn)['question_text']
answers = mechanics.get_current_question_answers(db_conn=db_conn)
answers_text = [x['answer_text'] for x in answers]
data = {
    "question": question,
    "option_1_id": answers[0]['a_id'],
    "option_2_id": answers[1]['a_id'],
    "option_3_id": answers[2]['a_id'],
    "option_4_id": answers[3]['a_id'],
    "option_1_text": answers[0]['answer_text'],
    "option_2_text": answers[1]['answer_text'],
    "option_3_text": answers[2]['answer_text'],
    "option_4_text": answers[3]['answer_text'],
}

# Define routes for each section
@app.route('/')
def index():
    return render_template('index.html', data=data)


@app.route('/handle_submit_answer', methods=['POST'])
def handle_submit_answer():
    answer = request.form['answers']
    print(answer)
    return render_template('index.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)
