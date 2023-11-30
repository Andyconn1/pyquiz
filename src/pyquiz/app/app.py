from flask import Flask, render_template
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
    "option_1": answers_text[0],
    "option_2": answers_text[1],
    "option_3": answers_text[2],
    "option_4": answers_text[3],
}

# Define routes for each section
@app.route('/')
def index():
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
