from drf_yasg import openapi

# пример данных, передаваемых, если включить добавление опроса + вопросы с вариантами одним запросом (.logic / add_questions_and_answers)
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

create_poll = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'name': openapi.Schema(type=openapi.TYPE_STRING, description='имя опроса'),
        'date_starts': openapi.Schema(type=openapi.TYPE_STRING, description='дата начала. Пример: 2021-02-03'),
        'date_ends': openapi.Schema(type=openapi.TYPE_STRING, description='дата окончания. Пример: 2021-02-06'),
        'description': openapi.Schema(type=openapi.TYPE_STRING, description='описание'),
    })

example_poll_body = {
    "id": 36,
    "name": "update",
    "date_ends": "2021-02-06",
    "description": "description"
}

update_poll_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='id опроса'),
        'name': openapi.Schema(type=openapi.TYPE_STRING, description='имя опроса'),
        'date_ends': openapi.Schema(type=openapi.TYPE_STRING, description='дата окончания. Пример: 2021-02-06'),
        'description': openapi.Schema(type=openapi.TYPE_STRING, description='описание'),
    })

example_add_question = {
    "poll_id": 36,
    "name": "question name",
    "periodic_number": 1,
    "type": "ONE"
}

add_question = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'poll_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='id опроса'),
        'name': openapi.Schema(type=openapi.TYPE_STRING, description='текст вопроса'),
        'periodic_number': openapi.Schema(type=openapi.TYPE_INTEGER, description='порядковый номер вопроса'),
        'type': openapi.Schema(type=openapi.TYPE_STRING, description='тип (один из) "TEXT" / "ONE" / "MANY"',
                               default='TEXT'),
    })

example_update_question = {
    "question_id": 50,
    "name": "question name23",
    "periodic_number": 5,
    "type": "ONE"
}

update_question = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'question_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='id вопроса'),
        'name': openapi.Schema(type=openapi.TYPE_STRING, description='имя вопроса'),
        'periodic_number': openapi.Schema(type=openapi.TYPE_INTEGER, description='порядковый номер вопроса'),
        'type': openapi.Schema(type=openapi.TYPE_STRING, description='тип (один из) "TEXT" / "ONE" / "MANY"'),
    })

example_question_option = {
    "question_id": 50,
    "position": 1,
    "name": "Вариант 1"
}

add_question_option = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'question_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='id вопроса'),
        'position': openapi.Schema(type=openapi.TYPE_INTEGER, description='порядковый номер варианта ответа',
                                   default=1),
        'name': openapi.Schema(type=openapi.TYPE_STRING, description='текст варианта ответа'),
    })

example_update_question_option = {
    "option_id": 78,
    "position": 1,
    "name": "Вариант Один"
}

update_question_option = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'option_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='id варианта ответа на вопрос'),
        'position': openapi.Schema(type=openapi.TYPE_INTEGER, description='порядковый номер варианта ответа на вопрос'),
        'name': openapi.Schema(type=openapi.TYPE_STRING, description='название варианта ответа на вопрос'),
    })

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

add_user_answer = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'question_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='id вопроса'),
        'answer_option_id': openapi.Schema(type=openapi.TYPE_INTEGER,
                                           description='id варианта ответа или список id ответов'),
        'type': openapi.Schema(type=openapi.TYPE_STRING,
                               description='Текст только для текстовых ответов. Не обязательный')
    })
