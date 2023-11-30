from pyquiz.data.setup_db import get_database_connection, setup_db
from pyquiz.game import mechanics

def rebuild(db_path: str) -> None:
    db_conn = get_database_connection(db_path=db_path)
    setup_db(db_conn=db_conn)

def continue_game(db_path: str) -> None:
    db_conn = get_database_connection(db_path=db_path)
    end_of_quiz = end_of_quiz(db_conn=db_conn)
    if end_of_quiz:
        show_scores()
    else:
        question = mechanics.get_current_question(db_conn=db_conn)
        question_text = question['question_text']
        answers = mechanics.get_current_question_answers(db_conn=db_conn)
        answers_ids = [x['a_id'] for x in answers]
        answers_text = [x['answer_text'] for x in answers]
        options = ", ".join([') '.join(map(str, i)) for i in zip(answers_ids, answers_text)])
        selected_answer_id = input(question_text + "\n" + options)
        mechanics.submit_answer(db_conn=db_conn, selected_a_id=selected_answer_id)
        reveal_result()