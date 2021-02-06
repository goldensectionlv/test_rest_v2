from .models import *


def create_poll_object(poll_data):
    poll_created = Poll.objects.create(
        name=poll_data['name'],
        date_starts=poll_data['date_starts'],
        date_ends=poll_data['date_ends'],
        description=poll_data['description']
    )
    return poll_created


def add_questions_and_answers(poll, questions):
    for i in range(len(questions)):
        question = Question.objects.create(
            poll=poll,
            name=questions[i]['name'],
            periodic_number=questions[i]['periodic_number'],
            type=questions[i]['type']
        )
        answers = questions[i]['answers']
        for z in range(len(answers)):
            Answer.objects.create(
                poll=poll,
                question=question,
                name=answers[z]['name'],
                position=answers[z]['position']
            )
