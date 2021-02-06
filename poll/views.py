from django.db.models import Prefetch
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from . import personal_serializers
from . import serializers

"""Get info"""


@api_view(['GET'])
def get_poll(request, poll_id):
    poll = Poll.objects.prefetch_related('questions').prefetch_related('questions__answers').filter(id=poll_id).first()

    if poll is None:
        return Response(f'Опроса с id {poll_id} не найдено', status=status.HTTP_404_NOT_FOUND)

    serializer = serializers.PollSerializer(poll, many=False)

    return Response(serializer.data)


@api_view(['GET'])
def get_all_polls(request):
    poll = Poll.objects.order_by('-id').all().prefetch_related('questions').prefetch_related('questions__answers')
    serializer = serializers.PollSerializer(poll, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_user_polls(request, user_id):
    poll = Poll.objects.filter(questions__question_answers__user_id=user_id).order_by(
        '-id').distinct().prefetch_related('questions'). \
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


# пример данных, передаваемых, если включить добавление опроса + вопросы с вариантами одним запросом (+ add_questions_and_answers)
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


@swagger_auto_schema(method='post', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'name': openapi.Schema(type=openapi.TYPE_STRING, description='имя опроса'),
        'date_starts': openapi.Schema(type=openapi.TYPE_STRING, description='дата начала. Пример: 2021-02-03'),
        'date_ends': openapi.Schema(type=openapi.TYPE_STRING, description='дата окончания. Пример: 2021-02-06'),
        'description': openapi.Schema(type=openapi.TYPE_STRING, description='описание'),
    }))
@api_view(['POST'])
def create_poll(request):
    poll = create_poll_object(poll_data=request.data)
    # add_questions_and_answers(poll=poll, questions=request.data['questions'])
    serializer = serializers.PollSerializer(poll, many=False)
    return Response(serializer.data)


example_poll_body = {
    "id": 36,
    "name": "update",
    "date_ends": "2021-02-06",
    "description": "description"
}


@swagger_auto_schema(method='post', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='id опроса'),
        'name': openapi.Schema(type=openapi.TYPE_STRING, description='имя опроса'),
        'date_ends': openapi.Schema(type=openapi.TYPE_STRING, description='дата окончания. Пример: 2021-02-06'),
        'description': openapi.Schema(type=openapi.TYPE_STRING, description='описание'),
    }))
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

    serializer = serializers.PollBodySerializer(poll, many=False)
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


@swagger_auto_schema(method='post', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'poll_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='id опроса'),
        'name': openapi.Schema(type=openapi.TYPE_STRING, description='текст вопроса'),
        'periodic_number': openapi.Schema(type=openapi.TYPE_INTEGER, description='порядковый номер вопроса'),
        'type': openapi.Schema(type=openapi.TYPE_STRING, description='тип (один из) "TEXT" / "ONE" / "MANY"',
                               default='TEXT'),
    }))
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


@swagger_auto_schema(method='post', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'question_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='id вопроса'),
        'name': openapi.Schema(type=openapi.TYPE_STRING, description='имя вопроса'),
        'periodic_number': openapi.Schema(type=openapi.TYPE_INTEGER, description='порядковый номер вопроса'),
        'type': openapi.Schema(type=openapi.TYPE_STRING, description='тип (один из) "TEXT" / "ONE" / "MANY"'),
    }))
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


@swagger_auto_schema(method='post', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'question_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='id вопроса'),
        'position': openapi.Schema(type=openapi.TYPE_INTEGER, description='порядковый номер варианта ответа',
                                   default=1),
        'name': openapi.Schema(type=openapi.TYPE_STRING, description='текст варианта ответа'),
    }))
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


@swagger_auto_schema(method='post', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'option_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='id варианта ответа на вопрос'),
        'position': openapi.Schema(type=openapi.TYPE_INTEGER, description='порядковый номер варианта ответа на вопрос'),
        'name': openapi.Schema(type=openapi.TYPE_STRING, description='название варианта ответа на вопрос'),
    }))
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

example_add_user_answer = {
    "question_id": 53,
    "answer_option_id": [84, 85, 86, 83],
    "text": "optional for Text type of questions, empty if not text-type"
}

example_add_user_answer2 = {
    "question_id": 53,
    "answer_option_id": 51,
    "text": "optional for Text type of questions, empty if not text-type"
}


@swagger_auto_schema(method='post', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'question_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='id вопроса'),
        'answer_option_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='id варианта ответа'),
        'type': openapi.Schema(type=openapi.TYPE_STRING,
                               description='Текст только для текстовых ответов. Не обязательный')
    }))
@api_view(['POST'])
def add_user_answer(request):
    try:
        question = Question.objects.get(id=request.data['question_id'])
        answer = []
        if question.type == 'ONE' or question.type == 'TEXT':
            answer = Answer.objects.get(id=request.data['answer_option_id'])

            if UserAnswer.objects.filter(answer=answer).exists():
                return Response(f'Пользователь уже оставил ответ на этот вопрос')

    except Answer.DoesNotExist:
        return Response(f'Вариант ответа не найден', status.HTTP_404_NOT_FOUND)

    except Question.DoesNotExist:
        return Response(f'Вопрос не найден', status.HTTP_404_NOT_FOUND)

    if question.type == 'ONE':
        UserAnswer.objects.create(
            user=request.user,
            answer=answer,
            question=question,
            poll=question.poll
        )
    elif question.type == 'TEXT':
        UserAnswer.objects.create(
            user=request.user,
            answer=answer,
            question=question,
            poll=question.poll,
            text=request.data['text']
        )
    elif question.type == 'MANY':

        check_is_answered = UserAnswer.objects.filter(user=request.user, question=question)
        if len(check_is_answered) > 0:
            return Response('Пользователь уже оставил ответ на этот вопрос')

        list_of_ids = request.data['answer_option_id']
        options_ids = Answer.objects.filter(id__in=list_of_ids)

        for i in range(len(options_ids)):
            UserAnswer.objects.create(
                user=request.user,
                answer=options_ids[i],
                question=question,
                poll=question.poll
            )

    return Response('Ответ добавлен')
