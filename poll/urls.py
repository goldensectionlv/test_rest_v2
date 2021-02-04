from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('get_poll/<int:poll_id>', views.get_poll),
    path('get_all_polls', views.get_all_polls),
    path('get_users_polls/<int:user_id>', views.get_users_polls),

    path('create_poll', views.create_poll),
    path('update_poll_body', views.update_poll_body),
    path('delete_poll/<int:poll_id>', views.delete_poll),

    path('add_question', views.add_question),
    path('update_question', views.update_question),
    path('delete_question/<int:question_id>', views.delete_question),

    path('add_question_option', views.add_question_option),
    path('update_question_option', views.update_question_option),
    path('delete_question_option/<int:option_id>', views.delete_question_option)
]
