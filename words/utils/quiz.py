from words.models.quiz import Quiz, QuizStatus


def compute_status(quiz: Quiz) -> QuizStatus:
    nbr_questions_answered = len(
        [q for q in quiz.questions.all() if q.response_index is not None]
    )

    if nbr_questions_answered == 0:
        return QuizStatus.NOT_STARTED

    if nbr_questions_answered < len(quiz.questions.all()):
        return QuizStatus.PARTIALLY_COMPLETE

    return QuizStatus.COMPLETE
