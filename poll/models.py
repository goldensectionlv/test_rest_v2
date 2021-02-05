from django.contrib.auth.models import User
from django.db import models


class Poll(models.Model):
    name = models.CharField(max_length=255)
    date_starts = models.DateField()
    date_ends = models.DateField()
    description = models.TextField()

    def __str__(self):
        return str(self.id) + ' ' + self.name


class Question(models.Model):
    TEXT = 'TEXT'
    ONE = 'ONE'
    MANY = 'MANY'
    QUESTION_TYPE = [
        (TEXT, TEXT),
        (ONE, ONE),
        (MANY, MANY)
    ]
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='questions')
    name = models.CharField(max_length=255)
    periodic_number = models.IntegerField()
    type = models.CharField(max_length=255, choices=QUESTION_TYPE, default=TEXT)

    def __str__(self):
        return str(self.id)


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    position = models.IntegerField(default=1)
    name = models.CharField(max_length=255)

    def __str__(self):
        return 'Вопрос: ' + self.question.name + ' / ' + self.name


class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='user_answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question_answers', null=True)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='poll_user_answers', null=True)
    text = models.CharField(max_length=1024, blank=True, null=True)

    def __str__(self):
        return self.user.username + ' ответ:' + self.answer.name



