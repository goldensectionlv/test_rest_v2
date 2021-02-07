from django.db.models import Prefetch
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from . import personal_serializers
from . import serializers
from . import swagger_requests
from . import logic

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


@swagger_auto_schema(method='post', operation_description="Создание тела опроса",
                     request_body=swagger_requests.create_poll)
@api_view(['POST'])
def create_poll(request):
    poll = logic.create_poll_object(poll_data=request.data)
    # add_questions_and_answers(poll=poll, questions=request.data['questions'])
    serializer = serializers.PollSerializer(poll, many=False)
    return Response(serializer.data)


@swagger_auto_schema(method='post', operation_description="Обновления тела опроса",
                     request_body=swagger_requests.update_poll_body)
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


@api_view(['delete'])
def delete_poll(request, poll_id):
    try:
        poll = Poll.objects.get(id=poll_id)
        poll.delete()
        return Response(f'Опрос с id {poll_id} удален', status.HTTP_200_OK)
    except Poll.DoesNotExist:
        return Response(f'Опрос с id {poll_id} не найден', status.HTTP_404_NOT_FOUND)


"""END"""

"""create, update, delete QUESTION"""


@swagger_auto_schema(method='post', request_body=swagger_requests.add_question)
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


@swagger_auto_schema(method='post', request_body=swagger_requests.update_question)
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


@api_view(['delete'])
def delete_question(request, question_id):
    try:
        question = Question.objects.get(id=question_id)
        question.delete()
        return Response(f'Вопрос с id {question_id} удален', status.HTTP_200_OK)
    except Question.DoesNotExist:
        return Response(f'Вопрос с id {question_id} не найден', status.HTTP_404_NOT_FOUND)


"""END"""

"""create, update, delete QUESTION ANSWER option"""


@swagger_auto_schema(method='post', operation_description="Создание варианта ответа",
                     request_body=swagger_requests.add_question_option)
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


@swagger_auto_schema(method='post', operation_description="Изменение варианта ответа",
                     request_body=swagger_requests.update_question_option)
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


@api_view(['delete'])
def delete_question_option(request, option_id):
    try:
        answer = Answer.objects.get(id=option_id)
        answer.delete()
        return Response(f'Опция ответа с id {option_id} удалена')
    except Answer.DoesNotExist:
        return Response(f'Опция ответа с id {option_id} не найдена', status.HTTP_404_NOT_FOUND)


"""END"""


@swagger_auto_schema(method='post', request_body=swagger_requests.add_user_answer)
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
        bulk_list = []
        for i in range(len(options_ids)):
            bulk_list.append(
                (UserAnswer(user=request.user, answer=options_ids[i], question=question, poll=question.poll))
            )
        UserAnswer.objects.bulk_create(bulk_list)

    return Response('Ответ добавлен')
