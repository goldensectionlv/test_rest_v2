from django.db.models import Prefetch
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from . import personal_serializers
from . import base_serializers

"""Get info"""


@api_view(['GET'])
def get_poll(request, poll_id):
    poll = Poll.objects.prefetch_related('questions').prefetch_related('questions__answers').filter(id=poll_id).first()

    if poll is None:
        return Response(f'Опроса с id {poll_id} не найдено', status=status.HTTP_404_NOT_FOUND)

    serializer = base_serializers.PollSerializer(poll, many=False)

    return Response(serializer.data)


@api_view(['GET'])
def get_all_polls(request):
    poll = Poll.objects.order_by('-id').all().prefetch_related('questions').prefetch_related('questions__answers')
    serializer = base_serializers.PollSerializer(poll, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_users_polls(request, user_id):
    poll = Poll.objects.filter(poll_user_answers__user_id=user_id).all().prefetch_related('questions'). \
        prefetch_related('questions__answers').prefetch_related(Prefetch('questions__answers__user_answers',
                                                                         queryset=UserAnswer.objects.filter(
                                                                             user_id=user_id)))
    serializer = personal_serializers.PollSerializer(poll, many=True)

    return Response(serializer.data)


"""END"""

"""create, update, delete poll body"""


def create_poll_object(poll_data):
    poll_created = Poll.objects.create(
        name=poll_data['name'],
        date_starts=poll_data['date_starts'],
        date_ends=poll_data['date_ends'],
        description=poll_data['description']
    )
    return poll_created


def add_questions_and_answers(poll, questions):
    print(questions)
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


example_create_poll_object = {
    "poll": {
        "name": "str",
        "date_starts": "2021-02-03",
        "date_ends": "2021-02-02",
        "description": "str"
    },
    "questions": [
        {
            "name": "Первый вопрос",
            "periodic_number": 1,
            "type": "ONE",
            "answers": [
                {
                    "name": "yes",
                    "position": 1
                },
                {
                    "name": "no",
                    "position": 2
                }
            ]
        },
        {
            "name": "Второй вопрос",
            "periodic_number": 2,
            "type": "MANY",
            "answers": [
                {
                    "name": "1",
                    "position": 1
                },
                {
                    "name": "2",
                    "position": 2
                },
                {
                    "name": "3",
                    "position": 3
                },
                {
                    "name": "4",
                    "position": 4
                }
            ]
        },
        {
            "name": "Третий вопрос",
            "periodic_number": 3,
            "type": "ONE",
            "answers": [
                {
                    "name": "yes",
                    "position": 1
                },
                {
                    "name": "no",
                    "position": 2
                }
            ]
        },
        {
            "name": "Четвертный",
            "periodic_number": 4,
            "type": "ONE",
            "answers": [
                {
                    "name": "yes",
                    "position": 1
                },
                {
                    "name": "no",
                    "position": 2
                }
            ]
        }
    ]
}


@api_view(['POST'])
def create_poll(request):
    poll = create_poll_object(poll_data=request.data['poll'])
    add_questions_and_answers(poll=poll, questions=request.data['questions'])
    serializer = base_serializers.PollSerializer(poll, many=False)
    return Response(serializer.data)


example_poll_body = {
    "id": 36,
    "name": "update",
    "date_ends": "2021-02-06",
    "description": "description"
}


@api_view(['POST'])
def update_poll_body(request):
    try:
        poll = Poll.objects.get(id=request.data['id'])
    except Poll.DoesNotExist:
        return Response(f'Опрос с id {request.data["id"]} не найден', status.HTTP_404_NOT_FOUND)

    poll.name = request.data['name']
    poll.date_ends = request.data['date_ends']
    poll.description = request.data['description']
    poll.save()

    serializer = base_serializers.PollBodySerializer(poll, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def delete_poll(request, poll_id):
    try:
        poll = Poll.objects.get(id=poll_id)
        poll.delete()
        return Response(f'Опрос с id {poll_id} удален', status.HTTP_200_OK)
    except Poll.DoesNotExist:
        return Response(f'Опрос с id {poll_id} не найден', status.HTTP_404_NOT_FOUND)


"""END"""

"""create, update, delete QUESTION"""
example_question = {
    "poll_id": 36,
    "name": "question name",
    "periodic_number": 1,
    "type": "ONE"
}


@api_view(['POST'])
def add_question(request):
    try:
        poll = Poll.objects.get(id=request.data["poll_id"])
    except Poll.DoesNotExist:
        return Response(f'Опрос с id {request.data["poll_id"]} не найден', status.HTTP_404_NOT_FOUND)

    Question.objects.create(
        poll=poll,
        name=request.data["name"],
        periodic_number=request.data["periodic_number"],
        type=request.data["type"]
    )
    return Response('Вопрос добавлен')


example_update_question = {
    "question_id": 50,
    "name": "question name23",
    "periodic_number": 5,
    "type": "ONE"
}


@api_view(['POST'])
def update_question(request):
    try:
        question = Question.objects.get(id=request.data['question_id'])
    except Question.DoesNotExist:
        return Response(f'Вопрос с id {request.data["question_id"]} не найден', status.HTTP_404_NOT_FOUND)

    question.name = request.data['name']
    question.periodic_number = request.data['periodic_number']
    question.type = request.data['type']
    question.save()

    return Response('Вопрос обновлен')


@api_view(['GET'])
def delete_question(request, question_id):
    try:
        question = Question.objects.get(id=question_id)
        question.delete()
        return Response(f'Вопрос с id {question_id} удален', status.HTTP_200_OK)
    except Question.DoesNotExist:
        return Response(f'Вопрос с id {question_id} не найден', status.HTTP_404_NOT_FOUND)


"""END"""

"""create, update, delete QUESTION ANSWER option"""

example_question_option = {
    "question_id": 50,
    "position": 1,
    "name": "Вариант 1"
}


@api_view(['POST'])
def add_question_option(request):
    try:
        question = Question.objects.get(id=request.data['question_id'])
    except Question.DoesNotExist:
        return Response(f'Опция ответа с id {request.data["question_id"]} не найден', status.HTTP_404_NOT_FOUND)

    Answer.objects.create(
        question=question,
        name=request.data["name"],
        position=request.data["position"]
    )

    return Response('Опция ответа создана')


example_update_question_option = {
    "option_id": 78,
    "position": 1,
    "name": "Вариант Один"
}


@api_view(['POST'])
def update_question_option(request):
    try:
        answer = Answer.objects.get(id=request.data['question_id'])
    except Answer.DoesNotExist:
        return Response(f'Вопрос с id {request.data["question_id"]} не найден', status.HTTP_404_NOT_FOUND)

    answer.name = request.data['name']
    answer.position = request.data['position']
    answer.save()

    return Response('Опция ответа изменена')


@api_view(['GET'])
def delete_question_option(request, option_id):
    try:
        answer = Answer.objects.get(id=option_id)
        answer.delete()
        return Response(f'Опция ответа с id {option_id} удалена')
    except Answer.DoesNotExist:
        return Response(f'Опция ответа с id {option_id} не найдена', status.HTTP_404_NOT_FOUND)


"""END"""
