# Requirements

- setup two teams from a list of individuals
- persist the teams between sessions.
- serve a list of questions to users one-by-one
- serve a list of possible answers to users (A, B, C, D)
- allow teams to take turns. Team 1 gets the first question, then Team 2 gets the second question.
- the first attempt at an answer is taken by the "current" team. 2 points awarded for correct answer.
- the second attempt at a correct answer is taken by the other team. 1 point awarded for a correct answer.

- scores saved & persisted between sessions
- current question stored & persisted between sessions


# Design

- database
    - question & answers@
        - question table: q_id, question_text
        - answers table: q_id, a_id, answer_text, correct_flag
    - teams:
        - team_members table: u_id, name, team (1, 2, Null)
    - state:
        - current_question: q_id, current_team, guess_answer_id
        - score: q_id, answered_correct_flag

- Front End
    - Main menu
        - users
        - teams
        - current scores
        - start quiz
        - continue quiz
    - Member setup
        - Add member
        - Delete member
    - Team setup
        - List each member, provide options for team 1, team 2, null
        - Save button
    - Game screen
        - show:
            - question
            - possible answers (radio buttons)
            - submit button
            - current team
            - scores summary
            - next button
