from words.models.quiz import Quiz, QuizStatus


def compute_status(quiz: Quiz) -> QuizStatus:
    nbr_questions_answered = len(
        [q for q in quiz.questions.all() if q.response_duration is not None]
    )

    if nbr_questions_answered == 0:
        return QuizStatus.NOT_STARTED

    if nbr_questions_answered < len(quiz.questions.all()):
        return QuizStatus.PARTIALLY_COMPLETE

    return QuizStatus.COMPLETE


def compute_nbr_right_answers(quiz: Quiz) -> int:
    nbr = 0

    for question in quiz.questions.all():
        if question.response_index is None:
            continue

        proposal = next(
            (proposal for proposal in question.proposals.all() if proposal.index == question.response_index), None)

        if not proposal:
            continue

        if proposal.right_answer:
            nbr += 1

    return nbr