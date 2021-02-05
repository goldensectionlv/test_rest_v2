from django.contrib import admin
from .models import *


class UserAnswerAdmin(admin.ModelAdmin):
    model = UserAnswer
    readonly_fields = ['id', ]
    extra = 0


class AnswerInline(admin.TabularInline):
    model = Answer
    readonly_fields = ['id', ]
    extra = 0


class UserAnswerInline(admin.TabularInline):
    model = UserAnswer
    readonly_fields = ['id', ]
    extra = 0


class QuestionInline(admin.StackedInline):
    model = Question
    inlines = [AnswerInline, ]
    readonly_fields = ['id', ]
    extra = 0


class PollAdmin(admin.ModelAdmin):
    model = Poll
    inlines = [QuestionInline]
    readonly_fields = ['id', ]
    extra = 0


class QuestionAdmin(admin.ModelAdmin):
    model = Question
    inlines = [AnswerInline, UserAnswerInline]
    readonly_fields = ['id', ]
    extra = 0


admin.site.register(Poll, PollAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(UserAnswer, UserAnswerAdmin)
