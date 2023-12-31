from flask import Flask, render_template, request, redirect
from pyquiz.game import mechanics
from pyquiz.data.setup_db import get_database_connection
from pyquiz.main import rebuild
import pandas as pd
import plotly.express as px
from plotly import utils
from json import dumps

app = Flask(__name__)

DB_PATH = r"C:\Users\andyc\AppData\Local\Temp\pyquiz.db"


# Define routes for each section
@app.route('/end')
def end():
    data = {
        "plotly_scores": get_scores_fig_json(),
    }
    return render_template('end.html', data=data)


def get_scores_fig_json():
    db_conn = get_database_connection(db_path=DB_PATH)
    sql = """
        WITH scores_summary AS (
            SELECT 
                t_id, 
                SUM(answered_correct_flag) AS correct
            FROM scores 
            GROUP BY t_id
        ),
        join_with_teams AS (
            SELECT t.team_name, s.correct
            FROM scores_summary AS s
            LEFT JOIN teams AS t
                ON s.t_id=t.t_id
        )
        SELECT *
        FROM join_with_teams
    """
    df_scores = pd.read_sql(sql=sql, con=db_conn)
    fig_scores = px.bar(df_scores, x="team_name", y="correct")
    fig_scores_json = dumps(fig_scores, cls=utils.PlotlyJSONEncoder)
    return fig_scores_json


@app.route('/')
def index():
    db_conn = get_database_connection(db_path=DB_PATH)
    question = mechanics.get_current_question(db_conn=db_conn)['question_text']
    answers = mechanics.get_current_question_answers(db_conn=db_conn)
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
        "plotly_scores": get_scores_fig_json(),
    }
    return render_template('index.html', data=data)


@app.route('/handle_submit_answer', methods=['POST'])
def handle_submit_answer():
    if 'answers' not in request.form.keys():
        return redirect('/')
    answer_id = request.form['answers']
    db_conn = get_database_connection(db_path=DB_PATH)
    mechanics.submit_answer(db_conn=db_conn, selected_a_id=answer_id)
    end_of_quiz = mechanics.end_of_quiz(db_conn=db_conn)
    print("end_of_quiz", end_of_quiz)
    if mechanics.end_of_quiz(db_conn=db_conn) == True:
        print("is the end")
        return redirect('/end')
    return redirect('/')


@app.route('/handle_hard_restart', methods=['POST'])
def handle_hard_restart():
    rebuild(db_path=DB_PATH)
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
