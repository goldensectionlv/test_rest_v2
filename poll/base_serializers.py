from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import *


class UserAnswerSerializer(ModelSerializer):
    class Meta:
        model = UserAnswer
        fields = ['id', 'user']


class AnswerSerializer(ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'position', 'name']


class QuestionSerializer(ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'name', 'periodic_number', 'type', 'answers']


class PollSerializer(ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Poll
        fields = ['id', 'name', 'date_starts', 'date_ends', 'description', 'questions', ]


class PollBodySerializer(ModelSerializer):

    class Meta:
        model = Poll
        fields = ['id', 'name', 'date_starts', 'date_ends', 'description']
