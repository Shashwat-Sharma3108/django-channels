
from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST


def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if not current_question_id:
        bot_responses.append(BOT_WELCOME_MESSAGE)

    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        return [error]

    next_question, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses


def record_current_answer(answer, current_question_id, session):
    '''
    Validates and stores the answer for the current question to django session.
    '''
    if not session.get('answers'):
        session['answers'] = {}  # Initialize answers dictionary in session if not present

    # Store the answer for the current question in the session
    session['answers'][current_question_id] = answer
    return True, "Your Answer is recorded"


def get_next_question(current_question_id):
    '''
    Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.
    '''
    total_questions = len(PYTHON_QUESTION_LIST)
    
    if current_question_id >= total_questions - 1:
        # If current_question_id is the last question or out of range
        return "No more questions available", -1

    # Increment the current_question_id to get the next question
    next_question_id = current_question_id + 1
    next_question = PYTHON_QUESTION_LIST[next_question_id]
    return next_question, next_question_id


def generate_final_response(session):
    '''
    Creates a final result message including a score based on the answers
    by the user for questions in the PYTHON_QUESTION_LIST.
    '''
    answers = session.get('answers', {})
    score = 0
    correct_answers = {count: x.get("answer") for count,x in enumerate(PYTHON_QUESTION_LIST)}
    if answers:
        for count,answer in enumerate(answers):
            if correct_answers['answers'][count] == answer:
                score += 1
    else:
        return "Failed"
