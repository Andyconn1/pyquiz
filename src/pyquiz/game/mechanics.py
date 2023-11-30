import sqlite3


def get_current_question(db_conn: sqlite3.Connection) -> dict:
    response = db_conn.execute("""
        SELECT q_id, question_text FROM questions
        WHERE q_id=(SELECT MAX(q_id) FROM current_question)
    """).fetchone()
    question = {
        'q_id': response[0],
        'question_text': response[1]
    }
    return question


def end_of_quiz(db_conn: sqlite3.Connection) -> bool:
    try:
        max_q_id = db_conn.execute("""
            SELECT MAX(q_id) FROM questions
        """).fetchone()[0]
        
        current_q_id = db_conn.execute("""
            SELECT MAX(q_id) FROM current_question
        """).fetchone()[0]
    except:
        return True
    return current_q_id <= max_q_id


def get_current_team_id(db_conn: sqlite3.Connection) -> int:
    response = db_conn.execute("""
        SELECT t_id FROM current_question
    """).fetchone()
    return response[0]


def get_current_question_answers(db_conn: sqlite3.Connection) -> list:
    response = db_conn.execute("""
        SELECT a_id, answer_text, correct_flag FROM answers
        WHERE q_id=(SELECT MAX(q_id) FROM current_question)
    """).fetchall()
    answers = [{"a_id": x[0], "answer_text": x[1], "correct_flag": x[2]} for x in response]
    return answers


def get_current_question_correct_answer(db_conn: sqlite3.Connection) -> dict:
    response = db_conn.execute("""
        SELECT a_id, answer_text FROM answers
        WHERE 
            q_id=(SELECT MAX(q_id) FROM current_question)
            AND correct_flag=True
    """).fetchone()
    answer = {"a_id": response[0], "answer_text": response[1]}
    answer
    return answer


def move_to_next_question(db_conn: sqlite3.Connection) -> None:
    db_conn.execute("""
        UPDATE current_question
        SET 
            q_id = q_id + 1,
            t_id = 
                CASE  
                    WHEN t_id = 0 THEN 1
                    ELSE 0
                END 
    """)
    db_conn.commit()


def update_score(db_conn: sqlite3.Connection, q_id: int, t_id: int, answered_correct_flag: bool) -> None:
    db_conn.execute(f"""
        INSERT INTO scores
        VALUES ({q_id}, {t_id}, {answered_correct_flag});
    """)
    db_conn.commit()


def submit_answer(db_conn: sqlite3.Connection, selected_a_id: int):
    # get the current question
    current_question = get_current_question(db_conn=db_conn)

    # get the correct answer
    correct_answer = get_current_question_correct_answer(db_conn=db_conn)

    # get current team id
    current_team_id = get_current_team_id(db_conn=db_conn)

    # update score
    answered_correct_flag = int(selected_a_id) == correct_answer['a_id']
    update_score(db_conn=db_conn, q_id=current_question['q_id'], t_id=current_team_id, answered_correct_flag=answered_correct_flag)

    # move to next question
    move_to_next_question(db_conn=db_conn)

    # return (True / False, Correct Answer text)
    return (answered_correct_flag, correct_answer['answer_text'])
    