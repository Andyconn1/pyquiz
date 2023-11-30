import sqlite3
import pandas as pd


def get_database_connection(db_path: str):
    return sqlite3.connect(database=db_path)


def create_replace_table_teams(db_conn: sqlite3.Connection):
    df = pd.DataFrame({
        "t_id": [0, 1],
        "team_name":  [
            'Team A',
            'Team B',
        ],
    })
    df['u_id'] = df.index
    df.to_sql('teams', db_conn, if_exists="replace", index=False)


def create_replace_table_users(db_conn: sqlite3.Connection):
    df = pd.DataFrame({
        "user":  [
            'Andy Conn',
            'Chris Backhouse',
            'Laura Chang',
            'Leasha Buckley',
            'Sarah Trolley',
            'Owen Thomas',
        ],
        "t_id": [
            0,
            0,
            0,
            1,
            1,
            1,
        ],
    })
    df['u_id'] = df.index
    df.to_sql('users', db_conn, if_exists="replace", index=False)


def create_replace_table_questions(db_conn: sqlite3.Connection):
    df = pd.DataFrame({
        "question_text": [
            "What is the capital city of England?",
            "What is the capital city of Scotland?"
        ]
    })
    df['q_id'] = df.index
    df.to_sql('questions', db_conn, if_exists="replace", index=False)


def create_replace_table_answers(db_conn: sqlite3.Connection):
    # q_id, a_id, answer_text, correct_flag
    df = pd.DataFrame({
        "q_id": [*[0]*4, *[1]*4],
        "answer_text": [
            "London", "Edinburgh", "Paris", "Berlin", 
            "London", "Edinburgh", "Paris", "Berlin", 
        ],
        "correct_flag": [
            True, False, False, False,
            False, True, False, False,
        ],
    })
    df['a_id'] = df.index
    df.to_sql('answers', db_conn, if_exists="replace", index=False)


def create_replace_table_current_question(db_conn: sqlite3.Connection):
    # q_id, a_id, answer_text, correct_flag
    df = pd.DataFrame({
        "q_id": [0],
        "t_id": [0],
    })
    df.to_sql('current_question', db_conn, if_exists="replace", index=False)


def create_replace_table_scores(db_conn: sqlite3.Connection):
    db_conn.execute(
        """
        DROP TABLE IF EXISTS scores
        """
    )
    db_conn.execute(
        """
        CREATE TABLE scores (
            q_id INTEGER,
            t_id INTEGER,
            answered_correct_flag BOOLEAN
        )
        """
    )
    db_conn.commit()


def setup_db(db_conn: sqlite3.Connection):
    create_replace_table_teams(db_conn=db_conn)
    create_replace_table_users(db_conn=db_conn)
    create_replace_table_questions(db_conn=db_conn)
    create_replace_table_answers(db_conn=db_conn)
    create_replace_table_current_question(db_conn=db_conn)
    create_replace_table_scores(db_conn=db_conn)